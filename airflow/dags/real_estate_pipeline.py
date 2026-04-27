from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import boto3
import time
import logging

logger = logging.getLogger(__name__)

# ── Default args ──────────────────────────────────────────────────────────────

default_args = {
    "owner":            "realestate",
    "retries":          2,
    "retry_delay":      timedelta(minutes=5),
    "email":            ["devender20025090@gmail.com"],
    "email_on_failure": True,
    "email_on_retry":   False,
}

# ── Task functions ────────────────────────────────────────────────────────────

def run_scraper(**context):
    """Run scraper.py and push listing count to XCom."""
    import subprocess, json, os

    result = subprocess.run(
        ["python", "/opt/airflow/scraper.py"],
        capture_output=True, text=True, timeout=1800  # 30 min max
    )

    logger.info(result.stdout)
    if result.returncode != 0:
        logger.error(result.stderr)
        raise Exception(f"Scraper failed:\n{result.stderr}")

    # Parse total listings from scraped_data.json
    try:
        with open("/opt/airflow/scraped_data.json") as f:
            data = json.load(f)
        count = len(data)
    except:
        count = 0

    logger.info(f"Scraper finished: {count} listings")
    context["ti"].xcom_push(key="listing_count", value=count)
    return count


def check_scraper_output(**context):
    """Branch: if listings < 50 → alert, else continue."""
    count = context["ti"].xcom_pull(key="listing_count", task_ids="run_scraper")
    logger.info(f"Listing count: {count}")
    if count < 50:
        return "alert_low_listings"
    return "trigger_glue_job"


def trigger_glue(**context):
    """Start Glue ETL job and wait for completion."""
    import os
    glue    = boto3.client("glue", region_name=os.getenv("AWS_DEFAULT_REGION", "ap-south-1"))
    job     = os.getenv("GLUE_JOB_NAME", "realestate-tracker-bronze-to-silver")

    logger.info(f"Starting Glue job: {job}")
    response = glue.start_job_run(JobName=job)
    run_id   = response["JobRunId"]
    logger.info(f"Glue run ID: {run_id}")

    # Poll until done
    while True:
        status = glue.get_job_run(JobName=job, RunId=run_id)["JobRun"]["JobRunState"]
        logger.info(f"Glue status: {status}")
        if status == "SUCCEEDED":
            logger.info("Glue job succeeded ✅")
            return run_id
        if status in ("FAILED", "ERROR", "TIMEOUT", "STOPPED"):
            raise Exception(f"Glue job {status}: run_id={run_id}")
        time.sleep(30)


def run_dbt(**context):
    """Run dbt gold layer models."""
    import subprocess, os

    env = {
        **os.environ,   # inherit all existing env vars
        "PG_HOST":     os.getenv("PG_HOST", "host.docker.internal"),
        "PG_PORT":     os.getenv("PG_PORT", "5432"),
        "PG_DBNAME":   os.getenv("PG_DBNAME", "RealEstateDB"),
        "PG_USER":     os.getenv("PG_USER", "postgres"),
        "PG_PASSWORD": os.getenv("PG_PASSWORD", ""),
    }

    result = subprocess.run(
        ["dbt", "run", "--profiles-dir", "/opt/airflow/dbt", "--project-dir", "/opt/airflow/dbt"],
        capture_output=True, text=True, cwd="/opt/airflow", env=env
    )
    logger.info(result.stdout)
    if result.returncode != 0:
        logger.error(result.stderr)
        raise Exception(f"dbt failed:\n{result.stderr}")
    logger.info("dbt gold layer complete ✅")


def run_dbt_tests(**context):
    """Run dbt tests after models."""
    import subprocess, os

    env = {
        **os.environ,
        "PG_HOST":     os.getenv("PG_HOST", "host.docker.internal"),
        "PG_PORT":     os.getenv("PG_PORT", "5432"),
        "PG_DBNAME":   os.getenv("PG_DBNAME", "RealEstateDB"),
        "PG_USER":     os.getenv("PG_USER", "postgres"),
        "PG_PASSWORD": os.getenv("PG_PASSWORD", ""),
    }

    result = subprocess.run(
        ["dbt", "test", "--profiles-dir", "/opt/airflow/dbt", "--project-dir", "/opt/airflow/dbt"],
        capture_output=True, text=True, cwd="/opt/airflow", env=env
    )
    logger.info(result.stdout)
    if result.returncode != 0:
        logger.error(result.stderr)
        raise Exception(f"dbt tests failed:\n{result.stderr}")
    logger.info("dbt tests passed ✅")


def send_summary(**context):
    """Push daily summary to CloudWatch Logs."""
    import os, json

    count   = context["ti"].xcom_pull(key="listing_count", task_ids="run_scraper")
    run_dt  = context["ds"]  # YYYY-MM-DD

    logs = boto3.client("logs", region_name=os.getenv("AWS_DEFAULT_REGION", "ap-south-1"))
    log_group  = "/real-estate/scraper"
    log_stream = f"airflow/{run_dt}"

    # Create stream if not exists
    try:
        logs.create_log_stream(logGroupName=log_group, logStreamName=log_stream)
    except logs.exceptions.ResourceAlreadyExistsException:
        pass

    message = f"Pipeline complete | date={run_dt} | listings={count} | Uploaded {count} records"
    logs.put_log_events(
        logGroupName=log_group,
        logStreamName=log_stream,
        logEvents=[{"timestamp": int(time.time() * 1000), "message": message}]
    )
    logger.info(f"Summary sent to CloudWatch: {message}")


def alert_low_listings(**context):
    """SNS alert if scraper returned too few listings."""
    import os
    count  = context["ti"].xcom_pull(key="listing_count", task_ids="run_scraper")
    sns    = boto3.client("sns", region_name=os.getenv("AWS_DEFAULT_REGION", "ap-south-1"))
    topic  = os.getenv("SNS_TOPIC_ARN", "")

    if topic:
        sns.publish(
            TopicArn=topic,
            Subject="⚠️ Real Estate Scraper — Low listing count",
            Message=f"Scraper only returned {count} listings on {context['ds']}. "
                    f"Check if sites have blocked scraping."
        )
    logger.warning(f"Low listing alert sent: {count} listings")

# ── DAG ───────────────────────────────────────────────────────────────────────

with DAG(
    dag_id="real_estate_pipeline",
    description="Scraper → S3 → Glue → dbt → CloudWatch",
    default_args=default_args,
    schedule_interval="0 2 * * *",   # 2:00 AM IST daily
    start_date=days_ago(1),
    catchup=False,
    tags=["realestate", "etl"],
) as dag:

    start = EmptyOperator(task_id="start")

    scrape = PythonOperator(
        task_id="run_scraper",
        python_callable=run_scraper,
    )

    check = BranchPythonOperator(
        task_id="check_scraper_output",
        python_callable=check_scraper_output,
    )

    alert = PythonOperator(
        task_id="alert_low_listings",
        python_callable=alert_low_listings,
    )

    glue = PythonOperator(
        task_id="trigger_glue_job",
        python_callable=trigger_glue,
    )

    dbt_run = PythonOperator(
        task_id="run_dbt",
        python_callable=run_dbt,
        trigger_rule="none_failed_min_one_success",
    )

    dbt_test = PythonOperator(
        task_id="run_dbt_tests",
        python_callable=run_dbt_tests,
    )

    summary = PythonOperator(
        task_id="send_summary",
        python_callable=send_summary,
        trigger_rule="none_failed_min_one_success",
    )

    end = EmptyOperator(
        task_id="end",
        trigger_rule="none_failed_min_one_success",
    )

    # ── DAG flow ──────────────────────────────────────────────────────────────
    start >> scrape >> check
    check >> alert >> end          # low listings branch
    check >> glue >> dbt_run >> dbt_test >> summary >> end