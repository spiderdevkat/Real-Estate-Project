import sys
import os
from datetime import datetime

# ✅ Tell Scrapy where settings are
os.environ.setdefault("SCRAPY_SETTINGS_MODULE", "apps.scraper.src.settings")

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from dotenv import load_dotenv

# ✅ Import spider classes (IMPORTANT)
from apps.scraper.src.spiders.nobroker import NoBrokerSpider
from apps.scraper.src.spiders.acres99_spider import Acres99Spider
from apps.scraper.src.spiders.magicbricks_spider import MagicBricksSpider

# ✅ Map source name → spider class
SPIDER_MAP = {
    "nobroker": NoBrokerSpider,
    "99acres": Acres99Spider,
    "magicbricks": MagicBricksSpider,
}

load_dotenv()


def main():
    cities = os.getenv("CITIES", "gurugram,delhi,bangalore").split(",")
    sources = os.getenv("SOURCES", "magicbricks,nobroker,99acres").split(",")

    print(f"🌍 Scraping {len(cities)} cities x {len(sources)} sources")

    today = datetime.now().strftime("%Y-%m-%d")
    bucket = os.getenv("S3_BRONZE", "my-bucket")

    settings = get_project_settings()
    settings.update({
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "DOWNLOAD_DELAY": float(os.getenv("SCRAPER_DELAY", 2)),
    })

    process = CrawlerProcess(settings)

    for city in cities:
        for source in sources:
            spider_class = SPIDER_MAP.get(source)

            if not spider_class:
                print(f"⚠️ Unknown source: {source}")
                continue

            feed_uri = (
                f"s3://{bucket}/raw/city={city}/source={source}"
                f"/date={today}/{source}_{city}.json"
            )

            print(f"🚀 Running {source} for {city}")

            process.crawl(
                spider_class,   # ✅ use class instead of string
                city=city,
                _feeds={
                    feed_uri: {
                        "format": "json",
                        "encoding": "utf-8",
                        "indent": 2,
                    }
                },
            )

    process.start()  # ✅ blocking call
    print("✅ Multi-city scrape complete!")


if __name__ == "__main__":
    main()