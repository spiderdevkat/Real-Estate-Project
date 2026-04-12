import asyncio
import json
import re
from datetime import date
from playwright.async_api import async_playwright

OUTPUT_FILE = "data/raw/magicbricks_listings.json"
URL = "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment&cityName=Gurgaon"

async def scrape(max_listings: int = 300):
    listings = []
    seen_titles = set()  # dedup tracker

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

        scroll_round = 0
        max_scrolls = 12  # 12 scrolls × ~15 new listings = ~180 listings
        no_new_count = 0  # stop if no new listings after 3 scrolls

        while scroll_round < max_scrolls and len(listings) < max_listings:
            # Extract all cards currently on page
            cards = await page.query_selector_all("div.mb-srp__card")
            new_this_round = 0

            for card in cards:
                try:
                    title_el   = await card.query_selector("h2.mb-srp__card--title")
                    full_title = await title_el.get_attribute("title") if title_el else None

                    # Skip if already seen
                    if not full_title or full_title in seen_titles:
                        continue
                    seen_titles.add(full_title)

                    price_el = await get_text(card, "div.mb-srp__card__price--amount")
                    ppsf_el  = await get_text(card, "div.mb-srp__card__price--size")
                    area_el  = await get_text(card, "div[data-summary='super-area'] div.mb-srp__card__summary--value")
                    url_el   = await get_attr(card, "h2.mb-srp__card--title a", "href")

                    item = {
                        "title":          full_title,
                        "price":          clean_price(price_el),
                        "price_per_sqft": clean_price(ppsf_el),
                        "area_sqft":      clean_number(area_el),
                        "locality":       extract_locality(full_title),
                        "city":           "gurugram",
                        "bhk":            extract_bhk(full_title),
                        "listing_date":   str(date.today()),
                        "source":         "magicbricks",
                        "url": f"https://www.magicbricks.com{url_el}" if url_el and url_el.startswith("/") else url_el,
                    }

                    listings.append(item)
                    new_this_round += 1

                except Exception as e:
                    continue

            print(f"  Scroll {scroll_round+1}: +{new_this_round} new | Total: {len(listings)}")
            # Save after every scroll — so we don't lose data
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                json.dump(listings, f, ensure_ascii=False, indent=2)

            # Stop if no new listings coming in
            if new_this_round == 0:
                no_new_count += 1
                if no_new_count >= 3:
                    print("  No new listings after 3 scrolls — stopping.")
                    break
            else:
                no_new_count = 0

            # Scroll down to load more
            await page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
            await page.wait_for_timeout(3000)  # wait for new listings to load
            scroll_round += 1

        await browser.close()

    print(f"\nTotal scraped: {len(listings)} listings")
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

def clean_price(raw_text):
    if not raw_text:
        return None
    try:
        # raw_text looks like "₹1.97 Cr" or "₹12,710 per sqft"
        raw_text = raw_text.replace("₹", "").replace(",", "").strip()
        # Extract number
        match = re.search(r"[\d.]+", raw_text)
        if not match:
            return None
        val = float(match.group())
        raw_lower = raw_text.lower()
        if "cr" in raw_lower:
            return int(round(val * 10000000))
        if "lac" in raw_lower or "lakh" in raw_lower:
            return int(round(val * 100000))
        return int(val)
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