import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import requests
import numpy as np
from typing import List, Dict
import plotly.figure_factory as ff

st.set_page_config(page_title="Real Estate Tracker", layout="wide", page_icon="🏠")

st.title("🏠 Real Estate Price Tracker")
st.markdown("**Gurugram Locality Rankings & Price Intelligence**")

# API calls
@st.cache_data(ttl=300)
def fetch_data(endpoint: str, params: Dict = None):
    try:
        response = requests.get(f"http://localhost:8000{endpoint}", params=params)
        return response.json()
    except:
        return []

# Fetch data
cities = fetch_data("/api/cities")
localities = fetch_data("/api/localities", {"city": "gurugram"})

if not localities:
    st.error("❌ API not running. Start FastAPI: `python -m uvicorn main:app --reload --port 8000`")
    st.stop()

# Filter valid data (price > 0)
valid_localities = [l for l in localities if l['avg_price_sqft'] > 1000]
valid_localities.sort(key=lambda x: x['avg_price_sqft'], reverse=True)

# Metrics
col1, col2, col3, col4 = st.columns(4)
total_listings = sum(l['listings'] for l in valid_localities)
avg_price = np.mean([l['avg_price_sqft'] for l in valid_localities[:20]])
top_locality = valid_localities[0]['locality'] if valid_localities else "N/A"

col1.metric("🏠 Total Localities", len(valid_localities))
col2.metric("📊 Total Listings", f"{total_listings:,}")
col3.metric("💰 Avg ₹/sqft", f"₹{avg_price:,.0f}")
col4.metric("🥇 Top Locality", top_locality)

# Top 10 Localities Table
st.subheader("🥇 Top Localities by Price/sqft")
df_top = pd.DataFrame(valid_localities[:15])
df_top['price_range'] = df_top.apply(lambda row: f"₹{row.min_price_sqft:,.0f} - ₹{row.max_price_sqft:,.0f}", axis=1)

st.dataframe(
    df_top[['locality', 'listings', 'avg_price_sqft', 'price_range']].round(0),
    use_container_width=True,
    column_config={
        "locality": st.column_config.TextColumn("Locality"),
        "listings": st.column_config.NumberColumn("Listings"),
        "avg_price_sqft": st.column_config.NumberColumn("₹/sqft", format="₹%,.0f"),
        "price_range": st.column_config.TextColumn("Price Range")
    }
)

# Price Distribution Chart
st.subheader("📈 Price Distribution")
fig = px.histogram(
    df_top.head(20), 
    x='avg_price_sqft',
    nbins=20,
    title="Top 20 Localities - Price/sqft Distribution",
    labels={'avg_price_sqft': '₹/sqft'}
)
fig.update_layout(showlegend=False, bargap=0.1)
st.plotly_chart(fig, width="stretch")

# Heatmap
st.subheader("🔥 Price Heatmap")
fig_heatmap = px.scatter(
    df_top.head(30),
    x='listings',
    y='locality',
    size='avg_price_sqft',
    color='avg_price_sqft',
    hover_data=['min_price_sqft', 'max_price_sqft'],
    color_continuous_scale='Viridis',
    title="Locality Heatmap: Size=Price/sqft, Color=Price/sqft"
)
st.plotly_chart(fig_heatmap, use_container_width=True)

# Stats Cards
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🏆 Most Expensive", f"₹{df_top['avg_price_sqft'].max():,.0f}/sqft")
with col2:
    st.metric("💎 Most Listings", f"{df_top['listings'].max()}")
with col3:
    st.metric("📍 Price Range", f"₹{df_top['avg_price_sqft'].min():,.0f} - ₹{df_top['avg_price_sqft'].max():,.0f}")

st.markdown("---")
st.markdown("**Built with ❤️ | Data from MagicBricks | Updated daily**")