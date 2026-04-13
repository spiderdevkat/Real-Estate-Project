import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "ap-south-1"),
)

bucket = "realestate-tracker-scripts-dev"
local_file = "apps/scraper/src/glue_bronze_to_silver.py"
s3_key = "scripts/bronze_to_silver.py"

print(f"Uploading {local_file} → s3://{bucket}/{s3_key}")
s3.upload_file(local_file, bucket, s3_key)
print("Script uploaded!")