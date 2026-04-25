import boto3
import json
import os
import hashlib
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────

S3_BRONZE = os.getenv("S3_BRONZE", "realestate-tracker-bronze-dev")
PG_URL    = (
    f"postgresql+psycopg2://postgres:{os.getenv('PG_PASSWORD')}"
    f"@localhost:5432/{os.getenv('PG_DATABASE')}"
)

# ── Helpers ───────────────────────────────────────────────────────────────────

def make_listing_hash(row: dict) -> str:
    url = str(row.get('url') or '').strip()
    
    if url and url.startswith('http'):
        # Stable URL exists — use it as identity
        key = f"{url}-{row.get('source','')}"
    else:
        # No URL — use title+price+city+source as identity
        # This means same listing at same price = same hash (SCD1 for these)
        key = (
            f"{row.get('title','notitle')}-"
            f"{row.get('price','0')}-"
            f"{row.get('city','')}-"
            f"{row.get('source','')}"
        )
    return hashlib.md5(key.encode()).hexdigest()

def make_record_hash(row: dict) -> str:
    """Fingerprint of mutable fields — changes when price/area updates."""
    key = f"{row.get('price') or ''}-{row.get('area_sqft') or ''}-{row.get('price_per_sqft') or ''}"
    return hashlib.md5(key.encode()).hexdigest()

def safe_int(val):
    try:    return int(float(val)) if val is not None else None
    except: return None

def safe_float(val):
    try:    return float(val) if val is not None else None
    except: return None

# ── Read bronze from S3 ───────────────────────────────────────────────────────

def read_bronze() -> pd.DataFrame:
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "ap-south-1"),
    )

    resp  = s3.list_objects_v2(Bucket=S3_BRONZE, Prefix="raw/")
    files = [o["Key"] for o in resp.get("Contents", []) if o["Key"].endswith(".json")]
    print(f"Found {len(files)} bronze files")

    frames = []
    for key in files:
        obj    = s3.get_object(Bucket=S3_BRONZE, Key=key)
        data   = json.loads(obj["Body"].read())
        df     = pd.DataFrame(data)
        source = key.split("source=")[1].split("/")[0]
        city   = key.split("city=")[1].split("/")[0]
        print(f"  {source:12} / {city:10} → {len(df)} records")
        frames.append(df)

    df_all = pd.concat(frames, ignore_index=True)
    print(f"\nTotal bronze records: {len(df_all)}")
    return df_all

# ── Clean ─────────────────────────────────────────────────────────────────────

def clean(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()

    # Price
    df["price"] = pd.to_numeric(df["price"], errors="coerce")
    df = df[df["price"].notna()]
    df = df[(df["price"] >= 500_000) & (df["price"] <= 5_000_000_000)]

    # Normalize text
    df["city"]   = df["city"].str.lower().str.strip()
    df["source"] = df["source"].str.lower().str.strip()
    df["title"]  = df["title"].str.strip() if "title" in df.columns else None
    df["locality"] = df["locality"].str.strip() if "locality" in df.columns else None

    # Dates
    df["listing_date"] = pd.to_datetime(df["ingested_at"], errors="coerce").dt.date

    print(f"After cleaning: {len(df)} records")
    return df

# ── SCD2 upsert ───────────────────────────────────────────────────────────────

def upsert_scd2(df: pd.DataFrame, engine):
    today     = datetime.utcnow().date()
    inserted  = 0
    updated   = 0
    unchanged = 0

    with engine.connect() as conn:
        for _, row in df.iterrows():
            r            = row.to_dict()
            listing_hash = make_listing_hash(r)
            record_hash  = make_record_hash(r)

            params = {
                "lh":          listing_hash,
                "rh":          record_hash,
                "title":       r.get("title"),
                "price":       safe_int(r.get("price")),
                "ppsf":        safe_float(r.get("price_per_sqft")),
                "area":        safe_float(r.get("area_sqft")),
                "locality":    r.get("locality"),
                "city":        r.get("city"),
                "bhk":         safe_int(r.get("bhk")),
                "source":      r.get("source"),
                "url":         r.get("url"),
                "today":       today,
                "ingested_at": r.get("ingested_at"),
            }

            # Check if listing exists in history
            existing = conn.execute(text("""
                SELECT id, record_hash, price
                FROM silver.listings_history
                WHERE listing_hash = :lh AND is_current = TRUE
            """), {"lh": listing_hash}).fetchone()

            if existing is None:
                # ── NEW listing ───────────────────────────────────────────────
                conn.execute(text("""
                    INSERT INTO silver.listings_history (
                        listing_hash, title, price, price_per_sqft, area_sqft,
                        locality, city, bhk, source, url,
                        effective_from, effective_to, is_current,
                        record_hash, ingested_at
                    ) VALUES (
                        :lh, :title, :price, :ppsf, :area,
                        :locality, :city, :bhk, :source, :url,
                        :today, NULL, TRUE,
                        :rh, :ingested_at
                    )
                """), params)
                inserted += 1

            elif existing.record_hash != record_hash:
                # ── PRICE/DETAILS CHANGED — close old, open new ───────────────
                conn.execute(text("""
                    UPDATE silver.listings_history
                    SET    effective_to = :today,
                           is_current   = FALSE
                    WHERE  listing_hash = :lh
                    AND    is_current   = TRUE
                """), {"today": today, "lh": listing_hash})

                conn.execute(text("""
                    INSERT INTO silver.listings_history (
                        listing_hash, title, price, price_per_sqft, area_sqft,
                        locality, city, bhk, source, url,
                        effective_from, effective_to, is_current,
                        record_hash, ingested_at
                    ) VALUES (
                        :lh, :title, :price, :ppsf, :area,
                        :locality, :city, :bhk, :source, :url,
                        :today, NULL, TRUE,
                        :rh, :ingested_at
                    )
                """), params)
                updated += 1

            else:
                # ── UNCHANGED — just bump last_seen ───────────────────────────
                unchanged += 1

        # ── Rebuild SCD1 current table from history ───────────────────────────
        conn.execute(text("TRUNCATE TABLE silver.listings_current"))
        conn.execute(text("""
            INSERT INTO silver.listings_current (
                listing_hash, title, price, price_per_sqft, area_sqft,
                locality, city, bhk, source, url,
                first_seen_date, last_seen_date
            )
            SELECT DISTINCT ON (listing_hash)
                listing_hash, title, price, price_per_sqft, area_sqft,
                locality, city, bhk, source, url,
                MIN(effective_from) OVER (PARTITION BY listing_hash),
                :today
            FROM silver.listings_history
            WHERE is_current = TRUE
            ON CONFLICT (listing_hash) DO UPDATE SET
                price           = EXCLUDED.price,
                last_seen_date  = EXCLUDED.last_seen_date,
                last_updated_at = NOW()
        """), {"today": today})

        conn.commit()

    print(f"\n  SCD2 results:")
    print(f"  ✅ New listings inserted : {inserted}")
    print(f"  🔄 Price changes detected: {updated}")
    print(f"  ⏭  Unchanged (skipped)   : {unchanged}")
    print(f"  Total processed          : {inserted + updated + unchanged}")

# ── Verify gold views ─────────────────────────────────────────────────────────

def verify(engine):
    with engine.connect() as conn:

        total = conn.execute(text(
            "SELECT COUNT(*) FROM silver.listings_history WHERE is_current = TRUE"
        )).scalar()
        print(f"\n── silver.listings_history (current) ── {total} records")

        print("\n── gold.city_price_summary ──────────────────────────────────")
        rows = conn.execute(text("""
            SELECT city, source, total_listings, avg_price, avg_price_per_sqft
            FROM gold.city_price_summary
            ORDER BY city, source
        """))
        for r in rows:
            ppsf = f"₹{r.avg_price_per_sqft:,.0f}/sqft" if r.avg_price_per_sqft else "no sqft data"
            print(f"  {r.city:12} | {r.source:12} | "
                  f"{r.total_listings:3} listings | "
                  f"avg ₹{r.avg_price:,.0f} | {ppsf}")

        print("\n── gold.bhk_price_summary ───────────────────────────────────")
        rows = conn.execute(text("""
            SELECT city, bhk, total_listings, avg_price, min_price, max_price
            FROM gold.bhk_price_summary
            ORDER BY city, bhk
        """))
        for r in rows:
            print(f"  {r.city:12} | {r.bhk}BHK | "
                  f"{r.total_listings:3} listings | "
                  f"avg ₹{r.avg_price:,.0f} | "
                  f"range ₹{r.min_price:,.0f}–₹{r.max_price:,.0f}")

        print("\n── gold.price_changes ───────────────────────────────")
        rows = conn.execute(text("""
            SELECT city, source, old_price, new_price, pct_change, delta
            FROM gold.price_changes
            LIMIT 10
        """))
        changes = list(rows)
        if changes:
            for r in changes:
                direction = "📈" if r.delta > 0 else "📉"
                print(f"  {direction} {r.city:10} | {r.source:12} | "
                      f"₹{r.old_price:,.0f} → ₹{r.new_price:,.0f} "
                      f"({r.pct_change:+.1f}%)")
        else:
            print("  (no changes yet)")

# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("Bronze → PostgreSQL (SCD2)")
    print("=" * 55)

    print("\n── Step 1: Read bronze from S3 ──────────────────────")
    df_raw = read_bronze()

    print("\n── Step 2: Clean ────────────────────────────────────")
    df_clean = clean(df_raw)

    print("\n── Step 3: Connect to PostgreSQL ────────────────────")
    engine = create_engine(PG_URL)
    print("✅ Connected")

    print("\n── Step 4: SCD2 upsert ──────────────────────────────")
    upsert_scd2(df_clean, engine)

    print("\n── Step 5: Verify gold views ────────────────────────")
    verify(engine)

    print("\n🎉 Done! Run this script daily after scraper.py")
    print("   Price changes will appear in gold.price_changes")