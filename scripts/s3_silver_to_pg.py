import pandas as pd
import psycopg2
from sqlalchemy import create_engine
import boto3
from io import BytesIO
import pyarrow.parquet as pq
import os
from dotenv import load_dotenv

load_dotenv()

# AWS Config
bucket = os.getenv('S3_SILVER')  # realestate-tracker-silver-dev
PG_PASSWORD = os.getenv('PG_PASSWORD')  # DevGsk_196795

print(f"📦 Bucket: {bucket}")
print(f"🗄️  DB: real_estate")

# PostgreSQL connection (FIXED DB NAME)
engine = create_engine(f'postgresql://postgres:{PG_PASSWORD}@localhost:5432/real_estate')

s3 = boto3.client('s3')

def list_silver_files():
    """List all Parquet files in Silver layer"""
    response = s3.list_objects_v2(Bucket=bucket, Prefix='cleaned/')
    files = []
    for obj in response.get('Contents', []):
        if obj['Key'].endswith('.parquet'):
            files.append(obj['Key'])
    return files

def load_parquet_to_postgres(s3_key):
    """Load single Parquet file to PostgreSQL"""
    print(f"   📥 {os.path.basename(s3_key)}")
    obj = s3.get_object(Bucket=bucket, Key=s3_key)
    parquet_file = pq.ParquetFile(BytesIO(obj['Body'].read()))
    
    df = parquet_file.read().to_pandas()
    print(f"     📊 Schema: {list(df.columns)}")
    
    # Fix data types
    numeric_cols = ['price', 'sqft', 'price_per_sqft', 'bhk']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    
    if 'scrape_date' in df.columns or 'listing_date' in df.columns:
        for date_col in ['scrape_date', 'listing_date']:
            if date_col in df.columns:
                df[date_col] = pd.to_datetime(df[date_col], errors='coerce').dt.date
    
    rows_loaded = len(df)
    df.to_sql('listings', engine, if_exists='append', index=False, method='multi')
    return rows_loaded

def main():
    files = list_silver_files()
    print(f"📁 Found {len(files)} Parquet files")
    
    if not files:
        print("❌ No parquet files found! Check S3 path.")
        return
    
    total_rows = 0
    for i, file in enumerate(files[:10]):  # Max 10 files for testing
        rows = load_parquet_to_postgres(file)
        total_rows += rows
        print(f"   ✅ {rows} rows (total: {total_rows})")
    
    # Verify load
    conn = psycopg2.connect(f"dbname=real_estate user=postgres password={PG_PASSWORD}")
    cur = conn.cursor()
    
    cur.execute("""
        CREATE INDEX IF NOT EXISTS idx_listings_city 
        ON listings(city);
    """)
    
    cur.execute("SELECT COUNT(*) FROM listings")
    final_count = cur.fetchone()[0]
    
    # REPLACE this broken query with:
    cur.execute("""
        SELECT city, COUNT(*) as listings, 
               ROUND(AVG(price_per_sqft)::numeric, 0) as avg_price_sqft
        FROM listings 
        GROUP BY city 
        ORDER BY avg_price_sqft DESC
    """)
    summary = cur.fetchall()
    
    conn.commit()
    cur.close()
    conn.close()
    
    print("\n" + "="*60)
    print(f"🎉 DAY 6 COMPLETE! {final_count:,} rows loaded to PostgreSQL")
    print("Summary by city:")
    for row in summary:
        print(f"  {row[0]:<15} {row[1]:>4} listings @ ₹{row[2]:>8,.0f}/sqft")
    print("="*60)

if __name__ == "__main__":
    main()