"""
Lambda function: realestate-data-validator
Trigger: S3 ObjectCreated on realestate-tracker-bronze-dev/raw/*
Purpose: Validate data quality on every bronze upload
"""

import json
import boto3
import os
import urllib.parse
from datetime import datetime

s3  = boto3.client("s3")
sns = boto3.client("sns", region_name=os.getenv("AWS_REGION", "ap-south-1"))

SNS_TOPIC_ARN = os.getenv("SNS_TOPIC_ARN", "")

# ── Thresholds ────────────────────────────────────────────────────────────────

RULES = {
    "min_records":       15,     # alert if fewer than this
    "max_null_price_pct": 40.0,  # alert if > 40% prices are null
    "min_avg_price":     500_000,     # 5 lakh minimum avg
    "max_avg_price":     500_000_000, # 50 Cr maximum avg
    "max_duplicate_pct": 50.0,   # alert if > 50% duplicates
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def load_json_from_s3(bucket: str, key: str) -> list:
    obj  = s3.get_object(Bucket=bucket, Key=key)
    data = json.loads(obj["Body"].read().decode("utf-8"))
    return data if isinstance(data, list) else []

def validate(data: list, source: str, city: str) -> dict:
    """Run all quality checks and return a report."""
    total     = len(data)
    issues    = []
    passed    = []

    # ── Check 1: Record count ─────────────────────────────────────────────────
    if total < RULES["min_records"]:
        issues.append(
            f"❌ LOW RECORD COUNT: {total} records (min: {RULES['min_records']})"
        )
    else:
        passed.append(f"✅ Record count: {total}")

    # ── Check 2: Null price rate ──────────────────────────────────────────────
    null_prices   = sum(1 for r in data if not r.get("price"))
    null_price_pct = (null_prices / total * 100) if total > 0 else 100
    if null_price_pct > RULES["max_null_price_pct"]:
        issues.append(
            f"❌ HIGH NULL PRICE RATE: {null_price_pct:.1f}% "
            f"({null_prices}/{total} records)"
        )
    else:
        passed.append(f"✅ Null price rate: {null_price_pct:.1f}%")

    # ── Check 3: Price range sanity ───────────────────────────────────────────
    prices = [float(r["price"]) for r in data
              if r.get("price") and str(r["price"]).replace(".","").isdigit()]
    if prices:
        avg_price = sum(prices) / len(prices)
        min_price = min(prices)
        max_price = max(prices)

        if avg_price < RULES["min_avg_price"]:
            issues.append(
                f"❌ AVG PRICE TOO LOW: ₹{avg_price:,.0f} "
                f"(min expected: ₹{RULES['min_avg_price']:,})"
            )
        elif avg_price > RULES["max_avg_price"]:
            issues.append(
                f"❌ AVG PRICE TOO HIGH: ₹{avg_price:,.0f} "
                f"(max expected: ₹{RULES['max_avg_price']:,})"
            )
        else:
            passed.append(
                f"✅ Price range: ₹{min_price:,.0f} – ₹{max_price:,.0f} "
                f"(avg ₹{avg_price:,.0f})"
            )
    else:
        issues.append("❌ NO VALID PRICES FOUND")

    # ── Check 4: Duplicate URL rate ───────────────────────────────────────────
    urls        = [r.get("url") for r in data if r.get("url")]
    unique_urls = set(urls)
    if urls:
        dup_pct = (1 - len(unique_urls) / len(urls)) * 100
        if dup_pct > RULES["max_duplicate_pct"]:
            issues.append(
                f"❌ HIGH DUPLICATE RATE: {dup_pct:.1f}% "
                f"({len(urls) - len(unique_urls)} duplicates)"
            )
        else:
            passed.append(f"✅ Duplicate rate: {dup_pct:.1f}%")
    else:
        passed.append("⚠️  No URLs to check (source may not provide URLs)")

    # ── Check 5: Required fields present ─────────────────────────────────────
    required = ["city", "source", "ingested_at"]
    for field in required:
        missing = sum(1 for r in data if not r.get(field))
        if missing > 0:
            issues.append(f"❌ MISSING FIELD '{field}': {missing}/{total} records")
        else:
            passed.append(f"✅ Field '{field}': all present")

    return {
        "source":     source,
        "city":       city,
        "total":      total,
        "issues":     issues,
        "passed":     passed,
        "status":     "FAILED" if issues else "PASSED",
        "checked_at": datetime.utcnow().isoformat(),
    }

def send_alert(report: dict, bucket: str, key: str):
    """Send SNS alert if validation failed."""
    if not SNS_TOPIC_ARN:
        print("⚠️  SNS_TOPIC_ARN not set — skipping alert")
        return

    subject = (
        f"🚨 Data Quality FAILED: {report['source']}/{report['city']}"
    )
    message = f"""
Real Estate Scraper — Data Quality Alert
==========================================
Source  : {report['source']}
City    : {report['city']}
Status  : {report['status']}
Records : {report['total']}
File    : s3://{bucket}/{key}
Time    : {report['checked_at']}

ISSUES FOUND:
{chr(10).join(report['issues'])}

CHECKS PASSED:
{chr(10).join(report['passed'])}
"""
    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject=subject,
        Message=message,
    )
    print(f"📧 Alert sent to SNS: {subject}")

# ── Lambda handler ────────────────────────────────────────────────────────────

def lambda_handler(event, context):
    results = []

    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key    = urllib.parse.unquote_plus(
            record["s3"]["object"]["key"]
        )

        print(f"\nValidating: s3://{bucket}/{key}")

        # Parse city and source from S3 key partition
        # e.g. raw/city=gurugram/source=magicbricks/date=2026-04-21/...
        try:
            parts  = {p.split("=")[0]: p.split("=")[1]
                      for p in key.split("/") if "=" in p}
            city   = parts.get("city",   "unknown")
            source = parts.get("source", "unknown")
        except Exception:
            city   = "unknown"
            source = "unknown"

        # Load and validate
        try:
            data   = load_json_from_s3(bucket, key)
            report = validate(data, source, city)
        except Exception as e:
            report = {
                "source":     source,
                "city":       city,
                "total":      0,
                "issues":     [f"❌ FAILED TO LOAD FILE: {str(e)}"],
                "passed":     [],
                "status":     "ERROR",
                "checked_at": datetime.utcnow().isoformat(),
            }

        # Print report
        print(f"\n── Validation Report: {source}/{city} ──")
        print(f"   Status : {report['status']}")
        print(f"   Records: {report['total']}")
        for p in report["passed"]:
            print(f"   {p}")
        for i in report["issues"]:
            print(f"   {i}")

        # Alert on failure
        if report["status"] in ("FAILED", "ERROR"):
            send_alert(report, bucket, key)

        results.append(report)

    # Summary
    failed = [r for r in results if r["status"] != "PASSED"]
    print(f"\n── Summary: {len(results)} files checked, {len(failed)} failed ──")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "checked": len(results),
            "failed":  len(failed),
            "results": results,
        })
    }


# ── Local test (run directly to test without Lambda) ─────────────────────────

if __name__ == "__main__":
    import os
    from dotenv import load_dotenv
    load_dotenv()

    # Simulate S3 event for all 9 bronze files
    TEST_BUCKET = os.getenv("S3_BRONZE", "realestate-tracker-bronze-dev")
    TEST_DATE   = datetime.now().strftime("%Y-%m-%d")

    s3_client = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "ap-south-1"),
    )

    # List actual files in bronze
    resp  = s3_client.list_objects_v2(Bucket=TEST_BUCKET, Prefix="raw/")
    files = [o["Key"] for o in resp.get("Contents", [])
             if o["Key"].endswith(".json")]

    print(f"Testing validator against {len(files)} bronze files...\n")

    # Build fake event
    fake_event = {
        "Records": [
            {
                "s3": {
                    "bucket": {"name": TEST_BUCKET},
                    "object": {"key": key},
                }
            }
            for key in files
        ]
    }

    result = lambda_handler(fake_event, None)
    body   = json.loads(result["body"])

    print(f"\n{'='*50}")
    print(f"FINAL: {body['checked']} checked, {body['failed']} failed")

    all_passed = [r for r in body["results"] if r["status"] == "PASSED"]
    all_failed = [r for r in body["results"] if r["status"] != "PASSED"]

    if all_passed:
        print(f"\n✅ PASSED ({len(all_passed)}):")
        for r in all_passed:
            print(f"   {r['source']:12} / {r['city']}")

    if all_failed:
        print(f"\n❌ FAILED ({len(all_failed)}):")
        for r in all_failed:
            print(f"   {r['source']:12} / {r['city']}")
            for issue in r["issues"]:
                print(f"      {issue}")