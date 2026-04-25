import psycopg2

try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="postgres",   # connect to default DB first
        user="postgres",
        password="DevGsk_196795",
    )
    conn.autocommit = True

    cur = conn.cursor()
    cur.execute('CREATE DATABASE "RealEstateDB"')

    cur.close()
    conn.close()

    print("✅ Database RealEstateDB created")

except Exception as e:
    print(f"❌ Error: {e}")