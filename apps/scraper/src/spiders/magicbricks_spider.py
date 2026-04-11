import scrapy
from scrapy_playwright.page import PageMethod
from datetime import date
import re

class MagicBricksSpider(scrapy.Spider):
    name = "magicbricks_gurugram"
    source = "magicbricks"
    city = "gurugram"

    async def start(self):
        url = "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment&cityName=Gurgaon"
        yield scrapy.Request(
            url=url,
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": [
                    PageMethod("wait_for_timeout", 5000),
                ],
            },
            callback=self.parse,
            errback=self.errback,
        )

    async def parse(self, response):
        page = response.meta.get("playwright_page")

        cards = response.css("div.mb-srp__card")
        self.logger.info(f"Found {len(cards)} listings on {response.url}")

        for card in cards:
            title    = card.css("h2.mb-srp__card--title a::text").get()
            price_raw  = card.css("div.mb-srp__card__price--amount::text").get()
            price_unit = card.css("div.mb-srp__card__price--size::text").get()
            ppsf_raw   = card.css("div.mb-srp__card__price--prpsqft::text").get()
            locality   = card.css("div.mb-srp__card__locality--name::text").get()
            area_raw   = card.css("div[data-summary='super-area'] div.mb-srp__card__summary--value::text").get()
            url        = card.css("h2.mb-srp__card--title a::attr(href)").get()

            item = {
                "title":          title.strip() if title else None,
                "price":          self.clean_price(price_raw, price_unit),
                "price_per_sqft": self.clean_number(ppsf_raw),
                "area_sqft":      self.clean_number(area_raw),
                "locality":       locality.strip() if locality else None,
                "city":           self.city,
                "bhk":            self.extract_bhk(title),
                "listing_date":   str(date.today()),
                "source":         self.source,
                "url": f"https://www.magicbricks.com{url}" if url and url.startswith("/") else (url or response.url),
            }

            self.logger.info(f"  → {item['title']} | ₹{item['price']} | {item['locality']}")
            yield item

        if page:
            await page.close()

    async def errback(self, failure):
        page = failure.request.meta.get("playwright_page")
        self.logger.error(f"Failed: {failure.request.url} — {failure.value}")
        if page:
            await page.close()

    def clean_price(self, amount, unit):
        if not amount:
            return None
        try:
            val = float(re.sub(r"[^\d.]", "", amount))
            if unit:
                u = unit.strip().lower()
                if "cr" in u:
                    return round(val * 10000000, 2)
                if "lac" in u or "lakh" in u:
                    return round(val * 100000, 2)
            return val
        except:
            return None

    def clean_number(self, raw):
        if not raw:
            return None
        try:
            return float(re.sub(r"[^\d.]", "", raw))
        except:
            return None

    def extract_bhk(self, title):
        if not title:
            return None
        m = re.search(r"(\d)\s*BHK", title, re.IGNORECASE)
        return int(m.group(1)) if m else None