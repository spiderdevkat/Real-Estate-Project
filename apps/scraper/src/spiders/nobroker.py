import scrapy
from scrapy_playwright.page import PageMethod
from datetime import datetime
import re

class NoBrokerSpider(scrapy.Spider):
    name = "nobroker"
    city = "gurugram"  # default fallback

    def __init__(self, city=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if city:
            self.city = city

    def start_requests(self):
        url = f"https://www.nobroker.in/property/buy-{self.city}/{self.city}"
        yield scrapy.Request(
            url=url,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod(
                        "add_init_script",
                        "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
                    ),
                    PageMethod("wait_for_timeout", 4000),
                ],
            },
            callback=self.parse,
            errback=self.errback,
        )

    async def parse(self, response):
        page = response.meta.get("playwright_page")

        cards = response.css("[data-cy='propertyCard']")
        self.logger.info(f"Found {len(cards)} listings on {response.url}")
        self.logger.debug(f"Response body preview: {response.text[:500]}")
        for card in cards[:20]:
            yield {
                "title":          card.css(".notForRentSale::text").get(),
                "price":          card.css("[data-cy='price']::text").get(),
                "price_per_sqft": card.css(".pp-sqft::text").get(),
                "area_sqft":      card.css(".size::text").get(),
                "locality":       card.css(".locality::text").get(),
                "city":           self.city,
                "bhk":            self.extract_bhk(card.css("::text").get()),
                "source":         "nobroker",
                "url":            card.css("a::attr(href)").get(),
                "ingested_at":    datetime.now().isoformat(),
            }
        
        # Next page
        # In parse(), before closing the page:
        if page:
            next_btn = await page.query_selector("button[aria-label='Go to next page']")
            if next_btn and await next_btn.is_enabled():
                await next_btn.click()
                await page.wait_for_timeout(3000)
                new_content = await page.content()
                # re-parse from new_content
            else:
                await page.close()

    async def errback(self, failure):
        page = failure.request.meta.get("playwright_page")
        self.logger.error(f"Failed: {failure.request.url} — {failure.value}")
        if page:
            await page.close()

    def extract_bhk(self, text):
        if not text:
            return None
        m = re.search(r"(\d)\s*(BHK|Bedroom)", text, re.IGNORECASE)
        return int(m.group(1)) if m else None