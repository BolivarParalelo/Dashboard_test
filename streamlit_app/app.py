import streamlit as st
import pandas as pd
from utils import api
import os

# --- Page Configuration ---
st.set_page_config(
    page_title="P2P Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom Dark Mode CSS ---
st.markdown("""
<style>
    /* General Body and Background */
    body {
        color: #e0e0e0;
        background-color: #1a1a2e; /* Deep purple-blue */
    }
    .stApp {
        background-color: #1a1a2e;
    }

    /* Sidebar */
    .st-emotion-cache-vk328u { /* Target sidebar background */
        background-color: #0f0f2c; /* Even darker blue */
    }
    .st-emotion-cache-vk328u .st-emotion-cache-1wivd7j { /* Sidebar text color */
        color: #e0e0e0;
    }

    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        color: #00bcd4; /* Cyan accent */
    }

    /* Text and Markdown */
    .st-emotion-cache-10trblm { /* Main content text */
        color: #e0e0e0;
    }
    .st-emotion-cache-1c7y2o2 { /* Markdown text */
        color: #e0e0e0;
    }

    /* Buttons */
    .stButton>button {
        background-color: #007bff; /* Blue accent */
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 20px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #0056b3; /* Darker blue on hover */
        color: white;
    }

    /* Input Fields (Text, Number, Selectbox) */
    .st-emotion-cache-1c7y2o2 input[type="text"],
    .st-emotion-cache-1c7y2o2 input[type="number"],
    .st-emotion-cache-1c7y2o2 .st-emotion-cache-10trblm { /* Selectbox input */
        background-color: #2c2c4a; /* Slightly lighter dark for inputs */
        color: #e0e0e0;
        border: 1px solid #6f42c1; /* Purple border */
        border-radius: 5px;
    }
    .st-emotion-cache-1c7y2o2 .st-emotion-cache-10trblm:focus {
        border-color: #00bcd4; /* Cyan focus */
        box-shadow: 0 0 0 0.2rem rgba(0, 188, 212, 0.25);
    }

    /* Dataframes */
    .st-emotion-cache-1c7y2o2 .st-emotion-cache-10trblm table {
        background-color: #2c2c4a; /* Dark background for table */
        color: #e0e0e0;
    }
    .st-emotion-cache-1c7y2o2 .st-emotion-cache-10trblm th { /* Table headers */
        background-color: #0f0f2c; /* Darker header background */
        color: #00bcd4; /* Cyan text for headers */
    }
    .st-emotion-cache-1c7y2o2 .st-emotion-cache-10trblm tr:nth-child(even) {
        background-color: #1a1a2e; /* Alternate row color */
    }
    .st-emotion-cache-1c7y2o2 .st-emotion-cache-10trblm tr:hover {
        background-color: #3a3a5a; /* Hover effect for rows */
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 1.2rem;
        color: #e0e0e0; /* Default tab text color */
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] [data-testid="stMarkdownContainer"] p {
        color: #00bcd4; /* Selected tab text color */
        font-weight: bold;
    }
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #0f0f2c; /* Tab background */
        border-radius: 5px 5px 0 0;
        margin-right: 5px;
        border-bottom: 3px solid transparent; /* Underline effect */
    }
    .stTabs [data-baseweb="tab-list"] button[aria-selected="true"] {
        border-bottom: 3px solid #00bcd4; /* Active tab underline */
        background-color: #1a1a2e; /* Active tab background */
    }

    /* Expander */
    .st-emotion-cache-1c7y2o2 .st-emotion-cache-10trblm .st-emotion-cache-10trblm { /* Expander header */
        background-color: #0f0f2c;
        border-radius: 5px;
        padding: 10px;
        color: #00bcd4;
    }
    .st-emotion-cache-1c7y2o2 .st-emotion-cache-10trblm .st-emotion-cache-10trblm:hover {
        background-color: #2c2c4a;
    }
    .st-emotion-cache-1c7y2o2 .st-emotion-cache-10trblm .st-emotion-cache-10trblm .st-emotion-cache-10trblm { /* Expander content */
        background-color: #1a1a2e;
        border-radius: 0 0 5px 5px;
        padding: 10px;
    }

    /* Metrics */
    [data-testid="stMetric"] {
        background-color: #0f0f2c;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #6f42c1;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
    [data-testid="stMetricLabel"] {
        color: #e0e0e0;
        font-size: 1.1em;
    }
    [data-testid="stMetricValue"] {
        color: #00bcd4;
        font-size: 2.5em;
        font-weight: bold;
    }
    [data-testid="stMetricDelta"] {
        color: #28a745; /* Green for positive delta */
    }

</style>
""", unsafe_allow_html=True)

# --- Sidebar for Global Controls ---
with st.sidebar:
    st.title("P2P Dashboard Controls")
    st.markdown("---")

    st.header("Global Filters")
    selected_exchange = st.selectbox(
        "Select Exchange",
        ("Binance", "Bybit"),
        help="Choose the cryptocurrency exchange to view offers from."
    )

# --- Main Content Area ---
st.title("📈 P2P Cryptocurrency Offer Dashboard")
st.markdown("Welcome to your comprehensive P2P trading insights. Select an exchange and apply filters to see real-time offers.")

# Check if API key is available from environment variable
api_key_from_env = os.getenv("P2P_DASHBOARD_API_KEY")

if not api_key_from_env:
    st.info("Please set the `P2P_DASHBOARD_API_KEY` environment variable to unlock the dashboard features.")
else:
    # Ensure API key from env is in session_state for consistency
    if 'api_key' not in st.session_state or st.session_state['api_key'] != api_key_from_env:
        st.session_state['api_key'] = api_key_from_env

    # --- Tabs for Exchanges ---
    tab_binance, tab_bybit = st.tabs(["Binance P2P Offers", "Bybit P2P Offers"])

    if selected_exchange == "Binance":
        with tab_binance:
            st.header("Binance P2P Offers")
            
            # Binance Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                binance_fiat = st.selectbox("Fiat Currency", ("USD", "NGN", "EUR"), key="binance_fiat")
            with col2:
                binance_asset = st.selectbox("Crypto Asset", ("USDT", "BTC", "ETH"), key="binance_asset")
            with col3:
                binance_trade_type = st.selectbox("Trade Type", ("BUY", "SELL"), key="binance_trade_type")

            if st.button("Fetch Binance Offers", key="fetch_binance"):
                with st.spinner("Fetching Binance offers..."):
                    binance_offers = api.get_binance_offers(binance_fiat, binance_asset, binance_trade_type)
                    if binance_offers:
                        df_binance = pd.DataFrame(binance_offers)
                        st.dataframe(df_binance, use_container_width=True)
                    else:
                        st.warning("No Binance offers found for the selected criteria or an error occurred.")

    elif selected_exchange == "Bybit":
        with tab_bybit:
            st.header("Bybit P2P Offers")
            
            # Bybit Filters
            col1, col2, col3 = st.columns(3)
            with col1:
                bybit_currency = st.selectbox("Fiat Currency", ("USD", "NGN", "EUR"), key="bybit_currency")
            with col2:
                bybit_token = st.selectbox("Crypto Asset", ("USDT", "BTC", "ETH"), key="bybit_token")
            with col3:
                bybit_side = st.selectbox("Trade Type", ("BUY", "SELL"), format_func=lambda x: "Buy" if x == "1" else "Sell", key="bybit_side")
                # Convert to API expected format
                bybit_side_api = "1" if bybit_side == "BUY" else "0"

            if st.button("Fetch Bybit Offers", key="fetch_bybit"):
                with st.spinner("Fetching Bybit offers..."):
                    bybit_offers = api.get_bybit_offers(bybit_currency, bybit_token, bybit_side_api)
                    if bybit_offers:
                        df_bybit = pd.DataFrame(bybit_offers)
                        st.dataframe(df_bybit, use_container_width=True)
                    else:
                        st.warning("No Bybit offers found for the selected criteria or an error occurred.")

    st.markdown("---")
    st.subheader("Market Insights (Coming Soon!)")
    st.write("This section will feature advanced visualizations and arbitrage opportunities.")