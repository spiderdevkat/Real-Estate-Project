import boto3
import json
import os
from datetime import date
from dotenv import load_dotenv

load_dotenv()

def upload_to_s3(local_file: str, bucket: str, s3_key: str):
    s3 = boto3.client(
        "s3",
        aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
        aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
        region_name=os.getenv("AWS_REGION", "ap-south-1"),
    )

    print(f"Uploading {local_file} → s3://{bucket}/{s3_key}")
    s3.upload_file(local_file, bucket, s3_key)
    print(f"Upload complete!")
    return f"s3://{bucket}/{s3_key}"

def get_s3_key(city: str, source: str) -> str:
    today = date.today()
    return f"raw/city={city}/source={source}/year={today.year}/month={today.month:02d}/day={today.day:02d}/listings.json"

if __name__ == "__main__":
    bucket = os.getenv("S3_BRONZE", "realestate-tracker-bronze-dev")
    city = "gurugram"
    source = "magicbricks"
    local_file = "data/raw/magicbricks_listings.json"
    s3_key = get_s3_key(city, source)
    upload_to_s3(local_file, bucket, s3_key)