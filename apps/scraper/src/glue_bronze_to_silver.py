import sys
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job
from pyspark.sql import functions as F
from pyspark.sql.types import *
from datetime import datetime

# Get job arguments
args = getResolvedOptions(sys.argv, [
    'JOB_NAME',
    'SOURCE_BUCKET',
    'TARGET_BUCKET',
    'SOURCE_PREFIX',
    'TARGET_PREFIX'
])

# Init Glue context
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

SOURCE_BUCKET = args['SOURCE_BUCKET']
TARGET_BUCKET = args['TARGET_BUCKET']
SOURCE_PREFIX = args['SOURCE_PREFIX']
TARGET_PREFIX = args['TARGET_PREFIX']

print(f"Reading from: s3://{SOURCE_BUCKET}/{SOURCE_PREFIX}")
print(f"Writing to:   s3://{TARGET_BUCKET}/{TARGET_PREFIX}")

# ── READ Bronze ──────────────────────────────────────────
# Read recursively from all partitions
df = spark.read \
    .option("multiline", "true") \
    .option("recursiveFileLookup", "true") \
    .json(f"s3://{SOURCE_BUCKET}/{SOURCE_PREFIX}")

print(f"Bronze records: {df.count()}")
df.printSchema()

# ── CLEAN Silver ─────────────────────────────────────────

# 1. Drop nulls in critical fields
df_clean = df.dropna(subset=["title", "price", "city"])

# 2. Fix data types
df_clean = df_clean.withColumn("price", F.col("price").cast(LongType()))
df_clean = df_clean.withColumn("price_per_sqft", F.col("price_per_sqft").cast(DoubleType()))
df_clean = df_clean.withColumn("area_sqft", F.col("area_sqft").cast(DoubleType()))
df_clean = df_clean.withColumn("bhk", F.col("bhk").cast(IntegerType()))
df_clean = df_clean.withColumn("listing_date", F.col("listing_date").cast(DateType()))

# 3. Add price_per_sqft if missing but we have price + area
df_clean = df_clean.withColumn(
    "price_per_sqft",
    F.when(
        F.col("price_per_sqft").isNull() & F.col("area_sqft").isNotNull(),
        F.round(F.col("price") / F.col("area_sqft"), 2)
    ).otherwise(F.col("price_per_sqft"))
)

# 4. Filter out bad prices
df_clean = df_clean.filter(
    (F.col("price") > 1000000) &   # min 10 lac
    (F.col("price") < 5000000000)  # max 500 Cr
)

# 5. Clean text fields
df_clean = df_clean.withColumn("title", F.trim(F.col("title")))
df_clean = df_clean.withColumn("locality", F.trim(F.col("locality")))
df_clean = df_clean.withColumn("city", F.lower(F.trim(F.col("city"))))

# 6. Deduplicate on title + listing_date
df_clean = df_clean.dropDuplicates(["title", "listing_date"])

# 7. Add ingestion timestamp
df_clean = df_clean.withColumn(
    "ingested_at",
    F.lit(datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")).cast(TimestampType())
)

print(f"Silver records after cleaning: {df_clean.count()}")

# ── WRITE Silver as Parquet ───────────────────────────────
output_path = f"s3://{TARGET_BUCKET}/{TARGET_PREFIX}city={df_clean.first()['city']}/source=magicbricks/"

df_clean.write \
    .mode("overwrite") \
    .partitionBy("listing_date") \
    .parquet(output_path)

print(f"Written to: {output_path}")
job.commit()