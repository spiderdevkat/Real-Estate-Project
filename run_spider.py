import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from apps.scraper.src.scraper import scrape
from apps.scraper.src.uploader import upload_to_s3, get_s3_key
from dotenv import load_dotenv

load_dotenv()

async def main():
    # Step 1 — Scrape
    print("=== STEP 1: SCRAPING ===")
    listings = await scrape()
    print(f"Scraped {len(listings)} listings")

    # Step 2 — Upload to S3 Bronze
    print("\n=== STEP 2: UPLOADING TO S3 ===")
    bucket = os.getenv("S3_BRONZE", "realestate-tracker-bronze-dev")
    s3_key = get_s3_key("gurugram", "magicbricks")
    s3_path = upload_to_s3("data/raw/magicbricks_listings.json", bucket, s3_key)
    print(f"Data live at: {s3_path}")

asyncio.run(main())