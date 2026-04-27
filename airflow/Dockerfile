FROM apache/airflow:2.9.1

USER root

# System packages needed for Playwright Chromium
RUN apt-get update && apt-get install -y \
    libglib2.0-0 \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Use python -m pip (safer in Airflow image)
RUN python -m pip install --no-cache-dir \
    playwright \
    boto3 \
    python-dotenv \
    dbt-postgres

# Install browser binaries
RUN python -m playwright install chromium