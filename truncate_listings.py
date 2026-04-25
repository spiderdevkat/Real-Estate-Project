import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname=os.getenv("PG_DATABASE"),
        user=os.getenv("PG_USER", "postgres"),
        password=os.getenv("PG_PASSWORD"),
    )
    conn.autocommit = True

    cur = conn.cursor()
    cur.execute("TRUNCATE TABLE silver.listings RESTART IDENTITY")

    cur.close()
    conn.close()

    print("✅ PostgreSQL silver.listings cleared")

except Exception as e:
    print(f"❌ Error: {e}")