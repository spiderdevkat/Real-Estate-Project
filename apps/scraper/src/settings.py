BOT_NAME = "realestate_scraper"

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "args": ["--no-sandbox"],
}
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 30000

DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 1
LOG_LEVEL = "INFO"

FEEDS = {
    "data/raw/magicbricks_listings.json": {
        "format": "json",
        "overwrite": True,
        "encoding": "utf8",
    }
}