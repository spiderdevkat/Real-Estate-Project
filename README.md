# Real Estate Project
🏠 Automated Indian real estate price tracker —  Scrapy → AWS S3/Glue/Redshift → FastAPI → Next.js dashboard.  Built with Airflow, Terraform & PySpark.

# 🏠 India Real Estate Price Tracker

> Track, analyse, and get alerted on real estate prices 
> across Indian cities — powered by a fully automated 
> data pipeline.

## 🎯 What This Does
- Scrapes listings daily from MagicBricks, 99acres, Housing.com
- Tracks price per sqft trends by locality over time
- Sends alerts when prices drop in your target area
- Exposes clean data via REST API for brokers & developers

## 🏙️ Cities Covered
Gurugram · Delhi NCR · Bengaluru *(expanding)*

## ⚙️ Tech Stack
| Layer | Technology |
|-------|-----------|
| Scraping | Scrapy + Playwright |
| Orchestration | Apache Airflow |
| Storage | AWS S3 (Bronze/Silver/Gold) |
| Pipeline | AWS Glue + Lambda |
| Warehouse | Amazon Redshift |
| API | FastAPI on AWS Lambda |
| Dashboard | Next.js + Recharts |
| IaC | Terraform |
| CI/CD | GitHub Actions |

## 🏗️ Architecture

Raw Scrape → S3 Bronze
→ Glue Clean → S3 Silver
→ Glue Aggregate → S3 Gold
→ Redshift Warehouse
→ FastAPI
→ Next.js Dashboard

## 📁 Project Structure

├── apps/
│   ├── scraper/       # Scrapy spiders
│   ├── api/           # FastAPI backend
│   └── dashboard/     # Next.js frontend
├── infra/
│   └── terraform/     # All AWS infrastructure
├── shared/            # Reusable utilities
└── configs/           # Environment configs

## 🚀 Status
🟡 In active development 

## 👨‍💻 Author
Devender Kataria — Data Engineer
[LinkedIn](https://linkedin.com/in/devender-kataria-a2516b1b9)