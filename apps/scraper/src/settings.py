BOT_NAME = "realestate_scraper"
SPIDER_MODULES = ["apps.scraper.src.spiders"]
NEWSPIDER_MODULE = "apps.scraper.src.spiders"

DOWNLOAD_HANDLERS = {
    "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
    "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
}

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"

PLAYWRIGHT_BROWSER_TYPE = "chromium"
PLAYWRIGHT_LAUNCH_OPTIONS = {
    "headless": True,
    "args": [
        "--no-sandbox",
        "--disable-blink-features=AutomationControlled",  # hide automation
        "--disable-dev-shm-usage",
        "--window-size=1920,1080",
    ],
}
PLAYWRIGHT_DEFAULT_NAVIGATION_TIMEOUT = 30000

# Add realistic headers
DEFAULT_REQUEST_HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-IN,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br",
    "Referer": "https://www.google.com/",
}

DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.useragent.UserAgentMiddleware": None,  # disable default
    "apps.scraper.src.middlewares.RotateUserAgentMiddleware": 400,
}

DOWNLOAD_DELAY = 3
RANDOMIZE_DOWNLOAD_DELAY = True
ROBOTSTXT_OBEY = False
CONCURRENT_REQUESTS = 1
LOG_LEVEL = "INFO"
