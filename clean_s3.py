# save as clean_s3.py and run once
import boto3, os
from dotenv import load_dotenv
load_dotenv()

s3 = boto3.client("s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "ap-south-1"),
)

bucket = os.getenv("S3_BRONZE", "realestate-tracker-bronze-dev")

# List all objects
resp = s3.list_objects_v2(Bucket=bucket, Prefix="raw/")
if "Contents" not in resp:
    print("Nothing to clean")
else:
    bad = []
    good = []
    for obj in resp["Contents"]:
        key = obj["Key"]
        # Good key has exactly: date=YYYY-MM-DD (10 chars after date=)
        if "/date=" in key:
            date_part = key.split("/date=")[1].split("/")[0]
            if len(date_part) == 10:
                good.append(key)
            else:
                bad.append(key)
        else:
            bad.append(key)  # datee= or datte= won't have /date=

    print(f"Good keys: {len(good)}")
    print(f"Bad keys to delete: {len(bad)}")
    for key in bad:
        print(f"  Deleting: {key}")
        s3.delete_object(Bucket=bucket, Key=key)

    print("✅ Cleanup done")