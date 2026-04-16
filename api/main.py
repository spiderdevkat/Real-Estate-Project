from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List
import uvicorn

load_dotenv()
app = FastAPI(title="🏠 Real Estate API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

PG_PASSWORD = os.getenv('PG_PASSWORD')
engine = create_engine(f'postgresql://postgres:{PG_PASSWORD}@localhost:5432/real_estate')

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
                ROUND(AVG(price_per_sqft)::numeric, 0) as median_price  -- Simplified
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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)