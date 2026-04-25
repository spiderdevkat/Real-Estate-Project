import boto3
import os
import time
from dotenv import load_dotenv

load_dotenv()

glue = boto3.client(
    "glue",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "ap-south-1"),
)

JOB_NAME = "realestate-tracker-bronze-to-silver"

print(f"Starting Glue job: {JOB_NAME}")
response = glue.start_job_run(
    JobName=JOB_NAME,
    Arguments={
        "--SOURCE_BUCKET": os.getenv("S3_BRONZE", "realestate-tracker-bronze-dev"),
        "--TARGET_BUCKET": os.getenv("S3_SILVER", "realestate-tracker-silver-dev"),
        "--SOURCE_PREFIX":  "raw/",
        "--TARGET_PREFIX":  "silver/",
        "--job-bookmark-option": "job-bookmark-disable",
    }
)
run_id = response["JobRunId"]
print(f"Job Run ID: {run_id}")

print("Waiting for job to complete...")
while True:
    status = glue.get_job_run(JobName=JOB_NAME, RunId=run_id)
    state  = status["JobRun"]["JobRunState"]
    print(f"  Status: {state}")
    if state in ["SUCCEEDED", "FAILED", "STOPPED", "ERROR"]:
        break
    time.sleep(30)

if state == "SUCCEEDED":
    print("\n✅ Glue job SUCCEEDED! Check S3 Silver bucket.")
else:
    error = status["JobRun"].get("ErrorMessage", "No error message")
    print(f"\n❌ Glue job {state}: {error}")