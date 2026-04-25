# v2 — fixed dedup + price filter
import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql.types import *
from datetime import datetime

args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'SOURCE_BUCKET',
    'TARGET_BUCKET',
    'SOURCE_PREFIX',
    'TARGET_PREFIX',
])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

SOURCE_BUCKET = args['SOURCE_BUCKET']
TARGET_BUCKET = args['TARGET_BUCKET']
SOURCE_PREFIX  = args['SOURCE_PREFIX']
TARGET_PREFIX  = args['TARGET_PREFIX']

print(f"Reading from: s3://{SOURCE_BUCKET}/{SOURCE_PREFIX}")
print(f"Writing to:   s3://{TARGET_BUCKET}/{TARGET_PREFIX}")

# ── READ all bronze partitions ────────────────────────────────────────────────
df = spark.read \
    .option("multiline", "true") \
    .option("recursiveFileLookup", "true") \
    .json(f"s3://{SOURCE_BUCKET}/{SOURCE_PREFIX}")

print(f"Bronze records read: {df.count()}")
df.printSchema()
df.show(5, truncate=False)

# ── CLEAN ─────────────────────────────────────────────────────────────────────

# 1. Drop rows where ALL critical fields are null (not just any one)
df = df.dropna(subset=["price", "city"], how="any")

# 2. Cast types
df = df \
    .withColumn("price",          F.col("price").cast(LongType())) \
    .withColumn("price_per_sqft", F.col("price_per_sqft").cast(DoubleType())) \
    .withColumn("area_sqft",      F.col("area_sqft").cast(DoubleType())) \
    .withColumn("bhk",            F.col("bhk").cast(IntegerType())) \
    .withColumn("ingested_at",    F.col("ingested_at").cast(TimestampType()))

# 3. listing_date — derive from ingested_at since scraper doesn't always set it
#    magicbricks sets listing_date, others don't — handle both
if "listing_date" in df.columns:
    df = df.withColumn(
        "listing_date",
        F.coalesce(
            F.col("listing_date").cast(DateType()),
            F.to_date(F.col("ingested_at"))
        )
    )
else:
    df = df.withColumn(
        "listing_date",
        F.to_date(F.col("ingested_at"))
    )

# 4. Derive price_per_sqft where missing but computable
df = df.withColumn(
    "price_per_sqft",
    F.when(
        F.col("price_per_sqft").isNull() & F.col("area_sqft").isNotNull() & (F.col("area_sqft") > 0),
        F.round(F.col("price") / F.col("area_sqft"), 2)
    ).otherwise(F.col("price_per_sqft"))
)

# 5. Price sanity filter
df = df.filter(
    (F.col("price") > 1_000_000) &
    (F.col("price") < 5_000_000_000)
)

# 6. Normalize text fields
df = df \
    .withColumn("title",    F.trim(F.col("title"))) \
    .withColumn("locality", F.trim(F.col("locality"))) \
    .withColumn("city",     F.lower(F.trim(F.col("city")))) \
    .withColumn("source",   F.lower(F.trim(F.col("source"))))

# 7. Deduplicate on url + source
df = df.dropDuplicates(["url", "source"])

# 8. Add silver processing timestamp
df = df.withColumn(
    "silver_processed_at",
    F.lit(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")).cast(TimestampType())
)

# 9. Select final silver schema
df_silver = df.select(
    "title",
    "price",
    "price_per_sqft",
    "area_sqft",
    "locality",
    "city",
    "bhk",
    "source",
    "url",
    "listing_date",
    "ingested_at",
    "silver_processed_at",
)

print(f"Silver records after cleaning: {df_silver.count()}")
df_silver.show(10, truncate=False)

# ── WRITE silver partitioned by city + source + listing_date ──────────────────
output_path = f"s3://{TARGET_BUCKET}/{TARGET_PREFIX}"

df_silver.write \
    .mode("overwrite") \
    .partitionBy("city", "source", "listing_date") \
    .parquet(output_path)

print(f"Silver written to: {output_path}")
job.commit()