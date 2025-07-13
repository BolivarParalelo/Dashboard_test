import requests
import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables from .env file

BASE_URL = "https://api.bolivarparalelo.org" # Assuming your FastAPI backend runs on this URL

def _get_headers():
    """Constructs headers with the API key from environment variable or session state."""
    api_key = os.getenv("P2P_DASHBOARD_API_KEY")
    if not api_key:
        api_key = st.session_state.get('api_key') # Fallback to session state if not in env

    if not api_key:
        st.error("API Key not found. Please set the GEMINI_API_KEY environment variable or enter it in the sidebar.")
        return None
    return {"X-API-Key": api_key}

@st.cache_data(ttl=300) # Cache data for 5 minutes
def get_binance_pairs():
    """Fetches available trading pairs from Binance."""
    headers = _get_headers()
    if not headers:
        return []
    try:
        response = requests.get(f"{BASE_URL}/api/v1/binance/pairs", headers=headers)
        response.raise_for_status() # Raise an HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Binance pairs: {e}")
        return []

@st.cache_data(ttl=60) # Cache offers for 1 minute
def get_binance_offers(fiat: str, asset: str, trade_type: str):
    """Fetches P2P offers from Binance."""
    headers = _get_headers()
    if not headers:
        return []
    params = {
        "fiat": fiat,
        "asset": asset,
        "trade_type": trade_type
    }
    try:
        response = requests.get(f"{BASE_URL}/api/v1/binance/offers", headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Binance offers: {e}")
        return []

@st.cache_data(ttl=60) # Cache offers for 1 minute
def get_bybit_offers(currency: str, token: str, side: str):
    """Fetches P2P offers from Bybit."""
    headers = _get_headers()
    if not headers:
        return []
    params = {
        "currency": currency,
        "token": token,
        "side": side
    }
    try:
        response = requests.get(f"{BASE_URL}/api/v1/bybit/offers", headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching Bybit offers: {e}")
        return []
