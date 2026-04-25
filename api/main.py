from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List, Dict
import uvicorn
from datetime import datetime, timedelta

load_dotenv()
app = FastAPI(title="🏠 Real Estate API", version="1.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000", "http://localhost:8501"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PG_PASSWORD = os.getenv('PG_PASSWORD')
engine = create_engine(f'postgresql://postgres:{PG_PASSWORD}@localhost:5432/real_estate')

# Models
class LocalitySummary(BaseModel):
    locality: str
    listings: int
    avg_price_sqft: float
    min_price_sqft: float
    max_price_sqft: float

class CityStats(BaseModel):
    total_listings: int
    avg_price_sqft: float
    min_price: float
    max_price: float
    median_price: float

class PriceTrend(BaseModel):
    locality: str
    date: str
    avg_price_sqft: float
    listings: int

class PriceAlert(BaseModel):
    locality: str
    current_price: float
    week_ago_price: float
    change_pct: float

# EXISTING ENDPOINTS (unchanged)
@app.get("/api/cities")
async def get_cities():
    with engine.connect() as conn:
        result = conn.execute(text("SELECT DISTINCT city FROM listings ORDER BY city"))
        return [{"city": row[0]} for row in result]

@app.get("/api/localities", response_model=List[LocalitySummary])
async def get_localities(city: str = Query(...)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                locality,
                COUNT(*) as listings,
                ROUND(AVG(price_per_sqft)::numeric, 0) as avg_price_sqft,
                MIN(price_per_sqft) as min_price_sqft,
                MAX(price_per_sqft) as max_price_sqft
            FROM listings 
            WHERE city ILIKE :city
            GROUP BY locality
            ORDER BY avg_price_sqft DESC
            LIMIT 50
        """), {"city": f"%{city}%"})
        
        return [
            LocalitySummary(
                locality=row[0], 
                listings=int(row[1]), 
                avg_price_sqft=float(row[2] or 0),
                min_price_sqft=float(row[3] or 0), 
                max_price_sqft=float(row[4] or 0)
            ) for row in result
        ]

@app.get("/api/stats", response_model=dict)
async def get_stats(city: str = Query(...)):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                COUNT(*) as total_listings,
                ROUND(AVG(price_per_sqft)::numeric, 0) as avg_price_sqft,
                MIN(price_per_sqft) as min_price,
                MAX(price_per_sqft) as max_price,
                ROUND(AVG(price_per_sqft)::numeric, 0) as median_price
            FROM listings 
            WHERE city ILIKE :city
        """), {"city": f"%{city}%"})
        row = result.fetchone()
        return {
            "total_listings": int(row[0]),
            "avg_price_sqft": float(row[1] or 0),
            "min_price": float(row[2] or 0),
            "max_price": float(row[3] or 0),
            "median_price": float(row[4] or 0)
        }

# NEW DAY 9: Price Trends (for charts)
@app.get("/api/trends", response_model=List[PriceTrend])
async def get_price_trends(locality: str = Query(...), city: str = Query(...)):
    """30-day price trends per locality"""
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                locality,
                DATE_TRUNC('day', ingested_at)::date as date,
                ROUND(AVG(price_per_sqft)::numeric, 0) as avg_price_sqft,
                COUNT(*) as listings
            FROM listings 
            WHERE locality ILIKE :locality AND city ILIKE :city
            GROUP BY locality, DATE_TRUNC('day', ingested_at)::date
            ORDER BY date DESC
            LIMIT 30
        """), {"locality": f"%{locality}%", "city": f"%{city}%"})
        
        return [
            PriceTrend(
                locality=row[0],
                date=row[1].isoformat() if row[1] else "",
                avg_price_sqft=float(row[2] or 0),
                listings=int(row[3])
            ) for row in result
        ]

# NEW DAY 9: Price Drop Alerts (PRO feature)
@app.get("/api/alerts", response_model=List[Dict])
async def get_price_alerts(city: str = Query(...), threshold_pct: float = Query(5.0)):
    """Localities with >5% price drop (7-day)"""
    with engine.connect() as conn:
        result = conn.execute(text("""
            WITH daily_avg AS (
                SELECT 
                    locality,
                    DATE_TRUNC('day', ingested_at)::date as date,
                    AVG(price_per_sqft) as avg_price
                FROM listings 
                WHERE city ILIKE :city AND price_per_sqft > 0
                GROUP BY locality, DATE_TRUNC('day', ingested_at)::date
            )
            SELECT 
                locality,
                MAX(CASE WHEN date = CURRENT_DATE THEN avg_price END) as current_price,
                MAX(CASE WHEN date = CURRENT_DATE - INTERVAL '7 days' THEN avg_price END) as week_ago_price,
                ROUND(
                    ((MAX(CASE WHEN date = CURRENT_DATE THEN avg_price END) - 
                      MAX(CASE WHEN date = CURRENT_DATE - INTERVAL '7 days' THEN avg_price END)) 
                     / MAX(CASE WHEN date = CURRENT_DATE - INTERVAL '7 days' THEN avg_price END) * 100)::numeric, 1
                ) as pct_change
            FROM daily_avg
            GROUP BY locality
            HAVING COUNT(*) >= 3 AND 
                   MAX(CASE WHEN date = CURRENT_DATE - INTERVAL '7 days' THEN avg_price END) IS NOT NULL
            ORDER BY pct_change ASC
            LIMIT 10
        """), {"city": f"%{city}%"})
        
        alerts = []
        for row in result:
            change_pct = float(row[3] or 0)
            if change_pct < -threshold_pct:  # Price DROP
                alerts.append({
                    "locality": row[0],
                    "current_price": float(row[1] or 0),
                    "week_ago_price": float(row[2] or 0),
                    "change_pct": change_pct,
                    "status": "🔴 PRICE DROP!"
                })
        return alerts

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)