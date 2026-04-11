from pydantic import BaseModel, validator
from typing import Optional
from datetime import date

class PropertyListing(BaseModel):
    title: Optional[str]
    price: Optional[float]
    price_per_sqft: Optional[float]
    area_sqft: Optional[float]
    locality: Optional[str]
    city: str
    bhk: Optional[int]
    listing_date: str
    source: str
    url: str

    @validator("price", pre=True)
    def clean_price(cls, v):
        if v is None:
            return None
        # Remove ₹, commas, "Lac", "Cr" etc
        v = str(v).replace("₹", "").replace(",", "").strip()
        if "Cr" in v or "cr" in v:
            v = v.replace("Cr", "").replace("cr", "").strip()
            return float(v) * 10000000
        if "Lac" in v or "lac" in v or "L" in v:
            v = v.replace("Lac", "").replace("lac", "").replace("L", "").strip()
            return float(v) * 100000
        try:
            return float(v)
        except:
            return None

    @validator("area_sqft", pre=True)
    def clean_area(cls, v):
        if v is None:
            return None
        v = str(v).replace("sq.ft.", "").replace("sqft", "").replace(",", "").strip()
        try:
            return float(v)
        except:
            return None

    @validator("bhk", pre=True)
    def clean_bhk(cls, v):
        if v is None:
            return None
        v = str(v)
        for num in ["1","2","3","4","5","6"]:
            if num in v:
                return int(num)
        return None