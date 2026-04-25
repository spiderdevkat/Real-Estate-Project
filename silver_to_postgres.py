import boto3
import pandas as pd
import pyarrow.parquet as pq
import pyarrow as pa
import io
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────

S3_SILVER  = os.getenv("S3_SILVER", "realestate-tracker-silver-dev")
SILVER_PREFIX = "silver/"

PG_HOST = os.getenv("PG_HOST",     "localhost")
PG_PORT = os.getenv("PG_PORT",     "5432")
PG_DB   = os.getenv("PG_DATABASE", "RealEstateDB")
PG_USER = os.getenv("PG_USER",     "postgres")
PG_PASS = os.getenv("PG_PASSWORD", "DevGsk_196795")

# ── S3 client ─────────────────────────────────────────────────────────────────

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION", "ap-south-1"),
)

# ── Read all parquet files from silver ───────────────────────────────────────

def read_silver_from_s3() -> pd.DataFrame:
    resp = s3.list_objects_v2(Bucket=S3_SILVER, Prefix=SILVER_PREFIX)

    if "Contents" not in resp:
        print("❌ No files found in silver/")
        return pd.DataFrame()

    frames = []
    for obj in resp["Contents"]:
        key = obj["Key"]
        if not key.endswith(".parquet"):
            continue

        print(f"  Reading: {key}")
        buffer = io.BytesIO()
        s3.download_fileobj(S3_SILVER, key, buffer)
        buffer.seek(0)

        table = pq.read_table(buffer)
        df = table.to_pandas()

        # Extract partition values from path if columns missing
        # e.g. silver/city=gurugram/source=magicbricks/listing_date=2026-04-19/
        parts = key.split("/")
        for part in parts:
            if "=" in part:
                col, val = part.split("=", 1)
                if col not in df.columns:
                    df[col] = val

        frames.append(df)

    if not frames:
        print("❌ No parquet files found")
        return pd.DataFrame()

    combined = pd.concat(frames, ignore_index=True)
    print(f"\n✅ Total records read from silver: {len(combined)}")
    return combined

# ── Setup PostgreSQL schemas + tables ─────────────────────────────────────────

def setup_postgres(engine):
    with engine.connect() as conn:
        # Create schemas
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS silver"))
        conn.execute(text("CREATE SCHEMA IF NOT EXISTS gold"))

        # Silver listings table
        conn.execute(text("""
            CREATE TABLE IF NOT EXISTS silver.listings (
                id                  SERIAL PRIMARY KEY,
                title               TEXT,
                price               BIGINT,
                price_per_sqft      DOUBLE PRECISION,
                area_sqft           DOUBLE PRECISION,
                locality            TEXT,
                city                TEXT,
                bhk                 INTEGER,
                source              TEXT,
                url                 TEXT,
                listing_date        DATE,
                ingested_at         TIMESTAMP,
                silver_processed_at TIMESTAMP,
                created_at          TIMESTAMP DEFAULT NOW()
            )
        """))

        # Unique constraint to prevent duplicate loads
        conn.execute(text("""
            CREATE UNIQUE INDEX IF NOT EXISTS idx_listings_url_source
            ON silver.listings (url, source)
            WHERE url IS NOT NULL
        """))

        # Gold: city price summary view
        conn.execute(text("""
            CREATE OR REPLACE VIEW gold.city_price_summary AS
            SELECT
                city,
                source,
                listing_date,
                COUNT(*)                        AS total_listings,
                ROUND(AVG(price))               AS avg_price,
                ROUND(MIN(price))               AS min_price,
                ROUND(MAX(price))               AS max_price,
                ROUND(AVG(price_per_sqft))      AS avg_price_per_sqft,
                ROUND(AVG(area_sqft))           AS avg_area_sqft
            FROM silver.listings
            WHERE price IS NOT NULL
            GROUP BY city, source, listing_date
            ORDER BY city, listing_date DESC
        """))

        # Gold: BHK breakdown view
        conn.execute(text("""
            CREATE OR REPLACE VIEW gold.bhk_price_summary AS
            SELECT
                city,
                bhk,
                COUNT(*)                   AS total_listings,
                ROUND(AVG(price))          AS avg_price,
                ROUND(AVG(price_per_sqft)) AS avg_price_per_sqft
            FROM silver.listings
            WHERE bhk IS NOT NULL AND price IS NOT NULL
            GROUP BY city, bhk
            ORDER BY city, bhk
        """))

        # Gold: locality hotspots view
        conn.execute(text("""
            CREATE OR REPLACE VIEW gold.locality_hotspots AS
            SELECT
                city,
                locality,
                COUNT(*)                   AS listings_count,
                ROUND(AVG(price))          AS avg_price,
                ROUND(AVG(price_per_sqft)) AS avg_price_per_sqft
            FROM silver.listings
            WHERE locality IS NOT NULL AND price IS NOT NULL
            GROUP BY city, locality
            HAVING COUNT(*) >= 2
            ORDER BY city, listings_count DESC
        """))

        conn.commit()
        print("✅ PostgreSQL schemas, tables and gold views created")

# ── Load into PostgreSQL ──────────────────────────────────────────────────────

def load_to_postgres(df: pd.DataFrame, engine):
    if df.empty:
        print("❌ No data to load")
        return

    # Keep only columns that exist in our table
    keep_cols = [
        "title", "price", "price_per_sqft", "area_sqft",
        "locality", "city", "bhk", "source", "url",
        "listing_date", "ingested_at", "silver_processed_at"
    ]
    df = df[[c for c in keep_cols if c in df.columns]]

    # Convert types
    for col in ["price"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    for col in ["price_per_sqft", "area_sqft"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
    for col in ["bhk"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    for col in ["listing_date", "ingested_at", "silver_processed_at"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Upsert — insert new, skip duplicates on url+source
    inserted = 0
    skipped  = 0
    for _, row in df.iterrows():
        try:
            row_dict = row.where(pd.notnull(row), None).to_dict()
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO silver.listings
                        (title, price, price_per_sqft, area_sqft, locality,
                         city, bhk, source, url, listing_date,
                         ingested_at, silver_processed_at)
                    VALUES
                        (:title, :price, :price_per_sqft, :area_sqft, :locality,
                         :city, :bhk, :source, :url, :listing_date,
                         :ingested_at, :silver_processed_at)
                    ON CONFLICT (url, source)
                    WHERE url IS NOT NULL
                    DO NOTHING
                """), row_dict)
                conn.commit()
            inserted += 1
        except Exception as e:
            skipped += 1
            print(f"  ⚠️ Skipped row: {e}")

    print(f"✅ Loaded {inserted} rows into silver.listings ({skipped} skipped/duplicates)")

# ── Query gold views to verify ────────────────────────────────────────────────

def verify_gold(engine):
    print("\n── gold.city_price_summary ──────────────────────────")
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT city, source, total_listings, avg_price, avg_price_per_sqft
            FROM gold.city_price_summary
        """))
        for row in result:
            print(f"  {row.city} | {row.source} | {row.total_listings} listings | "
                  f"avg ₹{row.avg_price:,} | ₹{row.avg_price_per_sqft}/sqft")

    print("\n── gold.bhk_price_summary ───────────────────────────")
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT city, bhk, total_listings, avg_price
            FROM gold.bhk_price_summary
            LIMIT 10
        """))
        for row in result:
            print(f"  {row.city} | {row.bhk}BHK | {row.total_listings} listings | avg ₹{row.avg_price:,}")

# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("── Step 1: Read silver from S3 ──────────────────────")
    df = read_silver_from_s3()

    if df.empty:
        print("No data. Exiting.")
        exit(1)

    print(f"\nSample data:")
    print(df[["title", "price", "city", "source"]].head())

    print("\n── Step 2: Connect to PostgreSQL ────────────────────")
    engine = create_engine(
        f"postgresql+psycopg2://{PG_USER}:{PG_PASS}@{PG_HOST}:{PG_PORT}/{PG_DB}"
    )
    print("✅ Connected to PostgreSQL")

    print("\n── Step 3: Setup schemas + tables ───────────────────")
    setup_postgres(engine)

    print("\n── Step 4: Load data ────────────────────────────────")
    load_to_postgres(df, engine)

    print("\n── Step 5: Verify gold views ────────────────────────")
    verify_gold(engine)

    print("\n🎉 Pipeline complete: S3 Silver → PostgreSQL → Gold views ready")