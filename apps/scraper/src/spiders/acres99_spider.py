import scrapy
from scrapy_playwright.page import PageMethod
from datetime import datetime
import re

class Acres99Spider(scrapy.Spider):
    name = "99acres"
    cities = ["Gurgaon", "Delhi", "Bangalore"]

    def start_requests(self):
        for city in self.cities:
            url = f"https://www.99acres.com/property-in-{city.lower().replace(' ', '-')}-ffid"
            yield scrapy.Request(
                  url=url,
                  meta={
                      "playwright": True,
                      "playwright_page_methods": [
                            PageMethod(
                                "add_init_script",
                                "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
                            ),
                            PageMethod("wait_for_timeout", 4000),
                        ],
                      "city": city   # 👈 merge here
                  },
                  callback=self.parse,
                  errback=self.errback,
            )

    async def parse(self, response):
        page = response.meta["playwright_page"]
        
        # 99acres CSS selectors
        cards = response.css(".srpTuple__projectTuple")
        self.logger.debug(f"Response body preview: {response.text[:500]}")
        for card in cards[:20]:
            title = card.css(".srpTuple__projectTitle::text").get()
            price = card.css(".priceRange::text").get()
            ppsf = card.css(".pricePerSqft::text").get()
            locality = card.css(".srpTuple__projectLocation::text").get()
            
            yield {
                'title': title.strip() if title else None,
                'price': self.clean_price(price),
                'price_per_sqft': self.clean_number(ppsf),
                'area_sqft': None,  # 99acres format
                'locality': locality.strip() if locality else None,
                'city': response.meta['city'],
                'bhk': self.extract_bhk(title),
                'source': '99acres',
                'url': response.urljoin(card.css('a::attr(href)').get() or ''),
                'ingested_at': datetime.now().isoformat()
            }
        
        await page.close()

    async def errback(self, failure):
        page = failure.request.meta.get("playwright_page")
        if page:
            await page.close()

    def clean_price(self, raw):
        if not raw: return None
        # "2.5 Cr" → 25000000
        if 'Cr' in raw: 
            return float(raw.split()[0]) * 10000000
        if 'L' in raw:
            return float(raw.split()[0]) * 100000
        return self.clean_number(raw)

    def clean_number(self, raw):
        if not raw: return None
        import re
        cleaned = re.sub(r"[^\d.]", "", raw)
        return float(cleaned) if cleaned else None

    def extract_bhk(self, title):
        if not title: return None
        import re
        m = re.search(r"(\d)\s*(BHK|Bedroom)", title, re.IGNORECASE)
        return int(m.group(1)) if m else None