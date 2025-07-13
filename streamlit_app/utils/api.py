import requests
import os
from dotenv import load_dotenv
import streamlit as st

# It's good practice to load environment variables for configuration
load_dotenv()

FASTAPI_BASE_URL = "http://127.0.0.1:8000"
# Load the API key from environment variables. Make sure it's set in your .env file
# or your deployment environment.
API_KEY = os.getenv("API_KEY")
HEADERS = {"X-API-Key": API_KEY}

@st.cache_data(ttl=3600)  # Cache pairs data for 1 hour
def get_binance_pairs():
    try:
        response = requests.get(f"{FASTAPI_BASE_URL}/api/v1/binance/pairs", headers=HEADERS)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Binance pairs: {e}")
        return []

@st.cache_data(ttl=60)  # Cache offers data for 1 minute
def get_binance_offers(fiat: str, asset: str, trade_type: str):
    try:
        response = requests.get(
            f"{FASTAPI_BASE_URL}/api/v1/binance/offers",
            params={"fiat": fiat, "asset": asset, "trade_type": trade_type},
            headers=HEADERS,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Binance offers: {e}")
        return []