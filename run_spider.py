import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from apps.scraper.src.scraper import scrape

asyncio.run(scrape())