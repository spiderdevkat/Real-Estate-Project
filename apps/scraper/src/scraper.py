import asyncio
import json
import re
from datetime import date
from playwright.async_api import async_playwright

OUTPUT_FILE = "data/raw/magicbricks_listings.json"
URL = "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment&cityName=Gurgaon"

async def scrape():
    listings = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            locale="en-IN",
            timezone_id="Asia/Kolkata",
        )
        page = await context.new_page()
        await page.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        print(f"Opening: {URL}")
        await page.goto(URL, wait_until="networkidle", timeout=60000)
        await page.wait_for_timeout(4000)

        # Get all cards
        cards = await page.query_selector_all("div.mb-srp__card")
        print(f"Found {len(cards)} listings")

        for card in cards:
            try:
                # Get title from the 'title' attribute — has full location info
                title_el  = await card.query_selector("h2.mb-srp__card--title")
                full_title = await title_el.get_attribute("title") if title_el else None
                price_el  = await get_text(card, "div.mb-srp__card__price--amount")
                unit_el   = await get_text(card, "div.mb-srp__card__price--size")
                ppsf_el   = await get_text(card, "div.mb-srp__card__price--prpsqft")
                area_el   = await get_text(card, "div[data-summary='super-area'] div.mb-srp__card__summary--value")
                url_el    = await get_attr(card, "h2.mb-srp__card--title a", "href")

                # Parse locality from title
                # Format: "3 BHK Flat for Sale in Society Name, Locality, City"
                locality = extract_locality(full_title)

                item = {
                    "title":          full_title,
                    "price":          clean_price(price_el, unit_el),
                    "price_per_sqft": clean_number(ppsf_el),
                    "area_sqft":      clean_number(area_el),
                    "locality":       locality,
                    "city":           "gurugram",
                    "bhk":            extract_bhk(full_title),
                    "listing_date":   str(date.today()),
                    "source":         "magicbricks",
                    "url": f"https://www.magicbricks.com{url_el}" if url_el and url_el.startswith("/") else url_el,
                }

                print(f"  → {item['bhk']} BHK | ₹{item['price']} | {item['locality']}")
                listings.append(item)

            except Exception as e:
                print(f"  Error on card: {e}")
            continue

        await browser.close()

    # Save to JSON
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(listings, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Saved {len(listings)} listings to {OUTPUT_FILE}")
    return listings


async def get_text(element, selector):
    el = await element.query_selector(selector)
    if el:
        text = await el.inner_text()
        return text.strip()
    return None

async def get_attr(element, selector, attr):
    el = await element.query_selector(selector)
    if el:
        return await el.get_attribute(attr)
    return None

def clean_price(amount, unit):
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

def clean_number(raw):
    if not raw:
        return None
    try:
        return float(re.sub(r"[^\d.]", "", raw))
    except:
        return None

def extract_bhk(title):
    if not title:
        return None
    m = re.search(r"(\d)\s*BHK", title, re.IGNORECASE)
    return int(m.group(1)) if m else None

def extract_locality(title):
    if not title:
        return None
    # Format: "X BHK Type for Sale in Society, Locality, City"
    try:
        # Split by " in " first
        parts = title.split(" in ", 1)
        if len(parts) < 2:
            return None
        # After "in": "Society Name, Locality, City"
        location_part = parts[1]
        segments = [s.strip() for s in location_part.split(",")]
        if len(segments) >= 2:
            # Second last segment is locality
            return segments[-2]
        return segments[0]
    except:
        return None
    
if __name__ == "__main__":
    asyncio.run(scrape())