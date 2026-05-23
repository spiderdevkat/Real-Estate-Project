# PropTrack India 🏠
> Real estate price intelligence across Gurugram, Delhi & Bangalore

**Live:** https://proptrack-india.vercel.app

## Architecture
Playwright Scraper → S3 Bronze → AWS Glue → S3 Silver (Parquet)
→ PostgreSQL SCD2 → dbt Gold Layer → Next.js Dashboard

## Stack
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-232F3E?style=flat&logo=amazonaws)
![dbt](https://img.shields.io/badge/dbt-FF694B?style=flat&logo=dbt)
![Airflow](https://img.shields.io/badge/Airflow-017CEE?style=flat&logo=apacheairflow)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat&logo=next.js)

## Key numbers
- 180+ listings/day scraped from 3 sources
- 155 records in SCD Type 2 history table
- 5 dbt models, 12 passing data tests
- Airflow DAG runs daily at 2AM IST
- 5 CloudWatch alarms + SNS email alerts

## Pipeline
| Layer | Technology | Purpose |
|-------|-----------|---------|
| Ingestion | Playwright + Python | Scrape 3 real estate sites |
| Bronze | AWS S3 (JSON) | Raw data, date-partitioned |
| Silver | AWS Glue + Parquet | Cleaned, normalised |
| Gold | PostgreSQL + dbt | Analytics-ready views |
| Orchestration | Airflow (Docker) | Daily scheduling |
| Validation | AWS Lambda | Auto-triggers on S3 upload |
| Monitoring | CloudWatch + SNS | Alerts on failures |
| Dashboard | Next.js + Vercel | Live at proptrack-india.vercel.app |
