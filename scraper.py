import asyncio
import json
import re
import warnings
import boto3
from datetime import datetime
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import os

warnings.filterwarnings("ignore")
load_dotenv()

# ── helpers ───────────────────────────────────────────────────────────────────

def extract_bhk(title):
    if not title: return None
    m = re.search(r"(\d)\s*BHK", title, re.IGNORECASE)
    return int(m.group(1)) if m else None

def clean_price(amount, unit=None):
    if not amount: return None
    try:
        val = float(re.sub(r"[^\d.]", "", str(amount)))
        if unit:
            u = unit.lower()
            if "cr" in u:                 return round(val * 10_000_000, 2)
            if "lac" in u or "lakh" in u: return round(val * 100_000, 2)
        a = str(amount).lower()
        if "cr" in a:  return round(val * 10_000_000, 2)
        if " l" in a:  return round(val * 100_000, 2)
        return val
    except: return None

def clean_number(raw):
    if not raw: return None
    try:    return float(re.sub(r"[^\d.]", "", str(raw)))
    except: return None

# ── S3 upload ─────────────────────────────────────────────────────────────────

def upload_to_s3(data: list, city: str, source: str):
    if not data:
        return
    s3     = boto3.client("s3")
    bucket = os.getenv("S3_BRONZE", "your-bucket-name")

    # Build date parts individually — no string formatting tricks
    now    = datetime.now()
    year   = str(now.year)         # "2026"
    month  = f"{now.month:02d}"    # "04"
    day    = f"{now.day:02d}"      # "20"
    today  = f"{year}-{month}-{day}"  # "2026-04-20"

    # Build key with explicit string concatenation — no f-string corruption
    key = "raw/city=" + city + "/source=" + source + "/date=" + today + "/" + source + "_" + city + ".json"

    print(f"  DEBUG → key: {key}")  # remove after confirming

    s3.put_object(
        Bucket=bucket,
        Key=key,
        Body=json.dumps(data, ensure_ascii=False, indent=2),
        ContentType="application/json",
    )
    # With this — verify from S3's response:
    print(f"  ☁️  Uploaded {len(data)} records → s3://{bucket}/{key}")
    print(f"  ✅ Actual S3 key used: {key}")  # key variable, not from boto3

# ── MagicBricks ───────────────────────────────────────────────────────────────

MAGICBRICKS_URLS = {
    "gurugram":  "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment&cityName=Gurgaon",
    "delhi":     "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment,Builder-Floor-Apartment,Penthouse,Studio-Apartment&cityName=New-Delhi",
    "bangalore": "https://www.magicbricks.com/property-for-sale/residential-real-estate?proptype=Multistorey-Apartment&cityName=Bangalore",
}

async def scrape_magicbricks(page, city: str) -> list:
    url = MAGICBRICKS_URLS[city.lower()]
    print(f"  [magicbricks] Loading {url}")
    await page.goto(url, wait_until="domcontentloaded", timeout=60_000)

    try:
        await page.wait_for_selector("div.mb-srp__card", timeout=15_000)
    except:
        await page.evaluate("window.scrollTo(0, 500)")
        await page.wait_for_timeout(5000)

    await page.evaluate("window.scrollTo(0, document.body.scrollHeight / 2)")
    await page.wait_for_timeout(2000)

    print(f"  [magicbricks] Title: {await page.title()}")
    cards = await page.query_selector_all("div.mb-srp__card")
    print(f"  [magicbricks] Cards found: {len(cards)}")

    if not cards:
        html = await page.content()
        with open(f"mb_{city}_debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  [magicbricks] ⚠️ saved mb_{city}_debug.html")
        return []

    results = []
    for card in cards[:20]:
        async def txt(sel, c=card):
            el = await c.query_selector(sel)
            return (await el.inner_text()).strip() if el else None
        async def attr(sel, a, c=card):
            el = await c.query_selector(sel)
            return await el.get_attribute(a) if el else None

        title      = await txt("h2.mb-srp__card--title a")
        price_raw  = await txt("div.mb-srp__card__price--amount")
        price_unit = await txt("div.mb-srp__card__price--size")
        ppsf_raw   = await txt("div.mb-srp__card__price--prpsqft")
        locality   = await txt("div.mb-srp__card__locality--name")
        area_raw   = await txt("div[data-summary='super-area'] div.mb-srp__card__summary--value")
        href       = await attr("h2.mb-srp__card--title a", "href")

        results.append({
            "title":          title,
            "price":          clean_price(price_raw, price_unit),
            "price_per_sqft": clean_number(ppsf_raw),
            "area_sqft":      clean_number(area_raw),
            "locality":       locality,
            "city":           city,
            "bhk":            extract_bhk(title),
            "source":         "magicbricks",
            "url":            f"https://www.magicbricks.com{href}" if href and href.startswith("/") else href,
            "ingested_at":    datetime.now().isoformat(),
        })
    return results

# ── 99acres ───────────────────────────────────────────────────────────────────

async def scrape_99acres(page, city: str) -> list:
    city_map = {"gurugram": "gurgaon", "delhi": "delhi", "bangalore": "bangalore"}
    url = f"https://www.99acres.com/flats-in-{city_map[city.lower()]}-ffid"
    print(f"  [99acres] Loading {url}")

    await page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    await page.wait_for_timeout(5000)

    # Scroll more aggressively to trigger lazy loading
    for scroll_y in [400, 800, 1200, 1600, 2000]:
        await page.evaluate(f"window.scrollTo(0, {scroll_y})")
        await page.wait_for_timeout(700)

    print(f"  [99acres] Title: {await page.title()}")

    cards = await page.evaluate("""
        () => {
            const all = [...document.querySelectorAll('div[id^="snb-"]')];
            
            // Fallback: top-level tuple divs if no snb- cards found
            const source = all.length > 0 ? all : (() => {
                const tuples = [...document.querySelectorAll('div[class*="tuple"]')];
                return tuples.filter(el => {
                    let parent = el.parentElement;
                    while (parent) {
                        if (parent.className?.includes?.('tuple')) return false;
                        parent = parent.parentElement;
                    }
                    return true;
                });
            })();

            return source.slice(0, 25).map(card => {
                // ── Title ──────────────────────────────────────────────────
                const titleEl = card.querySelector('a[data-label="CARD_TITLE"]')
                             || card.querySelector('[class*="cardHead"] a')
                             || card.querySelector('h2 a')
                             || card.querySelector('h2')
                             || card.querySelector('h3');
                const title = titleEl ? titleEl.innerText.trim() : null;

                // ── URL ────────────────────────────────────────────────────
                const linkEl = card.querySelector('a[data-label="CARD_TITLE"]')
                            || card.querySelector('a[href*="99acres"]')
                            || card.querySelector('a');
                const url = linkEl ? linkEl.getAttribute('href') : null;

                // ── Price: use data attributes & aria labels first ─────────
                // 99acres often stores price in data-price or aria-label
                let price = null;

                // 1. data-price attribute on card root or child
                const withDataPrice = card.querySelector('[data-price]');
                if (withDataPrice) price = withDataPrice.getAttribute('data-price');

                // 2. aria-label containing ₹ or "Cr" or "Lac"
                if (!price) {
                    const allEls = [...card.querySelectorAll('*')];
                    for (const el of allEls) {
                        const aria = el.getAttribute('aria-label') || '';
                        if (/[₹]|\\bCr\\b|\\bLac\\b|\\bLakh\\b/i.test(aria)) {
                            price = aria; break;
                        }
                    }
                }

                // 3. innerText of element whose text looks like a price
                if (!price) {
                    const allEls = [...card.querySelectorAll('*')];
                    for (const el of allEls) {
                        // Only look at leaf nodes (no children) to avoid grabbing parent text
                        if (el.children.length === 0) {
                            const t = el.innerText?.trim() || '';
                            if (/^[₹]?\\s*\\d+(\\.\\d+)?\\s*(Cr|Lac|Lakh|L\\b)/i.test(t)) {
                                price = t; break;
                            }
                        }
                    }
                }

                // ── Locality ───────────────────────────────────────────────
                let locality = null;
                const locEl = card.querySelector('[data-label="LOCALITY_LABEL"]')
                           || card.querySelector('[class*="locali"]')
                           || card.querySelector('[class*="Locali"]')
                           || card.querySelector('[class*="location"]');
                if (locEl) locality = locEl.innerText.trim();

                return { title, price_raw: price, locality, url };
            });
        }
    """)

    print(f"  [99acres] Cards extracted: {len(cards)}")

    results = []
    seen = set()

    for card in cards:
        title     = card.get("title")
        price_raw = card.get("price_raw")
        locality  = card.get("locality")
        href      = card.get("url")

        key = f"{title}-{price_raw}"
        if key in seen:
            continue
        seen.add(key)

        results.append({
            "title":          title,
            "price":          clean_price(price_raw),
            "price_per_sqft": None,
            "area_sqft":      None,
            "locality":       locality,
            "city":           city,
            "bhk":            extract_bhk(title),
            "source":         "99acres",
            "url":            href,
            "ingested_at":    datetime.now().isoformat(),
        })

    print(f"  [99acres] Unique listings: {len(results)}")
    return results

# ── Squareyards ───────────────────────────────────────────────────────────────

SQUAREYARDS_URLS = {
    "gurugram":  "https://www.squareyards.com/sale/property-for-sale-in-gurgaon",
    "delhi":     "https://www.squareyards.com/sale/property-for-sale-in-delhi",
    "bangalore": "https://www.squareyards.com/sale/property-for-sale-in-bangalore",
}

async def scrape_squareyards(page, city: str) -> list:
    url = SQUAREYARDS_URLS[city.lower()]
    print(f"  [squareyards] Loading {url}")

    await page.goto(url, wait_until="domcontentloaded", timeout=60_000)
    await page.wait_for_timeout(6000)

    for scroll_y in [400, 800, 1200, 1600]:
        await page.evaluate(f"window.scrollTo(0, {scroll_y})")
        await page.wait_for_timeout(800)

    print(f"  [squareyards] Title: {await page.title()}")

    cards_by_selector = {}
    for sel in [".project-card", "article"]:
        found = await page.query_selector_all(sel)
        real  = [el for el in found
                 if await el.evaluate("el => el.children.length") >= 2]
        cards_by_selector[sel] = real
        print(f"  [squareyards] {sel}: {len(real)} real cards")

    best_sel = max(cards_by_selector, key=lambda s: len(cards_by_selector[s]))
    cards    = cards_by_selector[best_sel]
    print(f"  [squareyards] ✅ Using '{best_sel}' → {len(cards)} cards")

    if not cards:
        html = await page.content()
        with open(f"squareyards_{city}_debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  [squareyards] ⚠️ saved squareyards_{city}_debug.html")
        return []

    results = []
    for card in cards[:20]:
        async def txt(sel, c=card):
            el = await c.query_selector(sel)
            return (await el.inner_text()).strip() if el else None
        async def attr(sel, a, c=card):
            el = await c.query_selector(sel)
            return await el.get_attribute(a) if el else None

        title    = (await txt("[class*='title']") or await txt("[class*='Title']")
                    or await txt("h2") or await txt("h3"))
        price    = (await txt("[class*='price']") or await txt("[class*='Price']")
                    or await txt("[class*='amount']") or await txt("[class*='Amount']"))
        locality = (await txt("[class*='location']") or await txt("[class*='locality']")
                    or await txt("[class*='address']") or await txt("[class*='area']"))
        href     = await attr("a", "href")

        results.append({
            "title":          title,
            "price":          clean_price(price),
            "price_per_sqft": None,
            "area_sqft":      None,
            "locality":       locality,
            "city":           city,
            "bhk":            extract_bhk(title),
            "source":         "squareyards",
            "url":            f"https://www.squareyards.com{href}" if href and href.startswith("/") else href,
            "ingested_at":    datetime.now().isoformat(),
        })
    return results

# ── config ────────────────────────────────────────────────────────────────────

SCRAPERS = {
    "magicbricks": scrape_magicbricks,
    "99acres":     scrape_99acres,
    "squareyards": scrape_squareyards,
}

CITIES  = os.getenv("CITIES",  "gurugram,delhi,bangalore").split(",")
SOURCES = os.getenv("SOURCES", "magicbricks,99acres,squareyards").split(",")

# ── main ──────────────────────────────────────────────────────────────────────

async def main():
    all_results = []

    async with async_playwright() as pw:
        browser = await pw.chromium.launch(
            headless=True,   # set to True for production
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--window-size=1400,900",
            ],
        )

        for city in CITIES:
            for source in SOURCES:
                print(f"\n{'='*50}")
                print(f"Scraping {source} / {city}")
                print(f"{'='*50}")

                # Fresh browser context per scrape prevents session fingerprinting
                context = await browser.new_context(
                    user_agent=(
                        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/124.0.0.0 Safari/537.36"
                    ),
                    viewport={"width": 1400, "height": 900},
                    locale="en-IN",
                )
                await context.add_init_script(
                    "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
                )
                page = await context.new_page()

                try:
                    results = await SCRAPERS[source](page, city)
                    print(f"  ✅ Got {len(results)} listings")
                    for r in results:
                        r["city"]   = city
                        r["source"] = source
                    upload_to_s3(results, city, source)
                    all_results.extend(results)
                except Exception as e:
                    print(f"  ❌ Error: {e}")
                    import traceback; traceback.print_exc()
                finally:
                    await context.close()

                await asyncio.sleep(3)

        await browser.close()

    with open("scraped_data.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)

    print(f"\n{'='*50}")
    print("FINAL SUMMARY")
    print(f"{'='*50}")
    by_key = {}
    for r in all_results:
        k = f"{r['source']} / {r['city']}"
        by_key[k] = by_key.get(k, 0) + 1
    for k, count in sorted(by_key.items()):
        status = "✅" if count >= 8 else "⚠️"
        print(f"  {status} {k}: {count} listings")
    print(f"\n  Total: {len(all_results)} listings → scraped_data.json")

if __name__ == "__main__":
    asyncio.run(main())