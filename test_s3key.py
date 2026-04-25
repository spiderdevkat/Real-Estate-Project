from datetime import datetime

today = datetime.now().strftime("%Y-%m-%d")
print("repr(today):", repr(today))
print("len(today):", len(today))

city = "gurugram"
source = "magicbricks"

key = f"raw/city={city}/source={source}/date={today}/{source}_{city}.json"
print("S3 key:", key)