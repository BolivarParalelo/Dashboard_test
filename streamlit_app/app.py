import streamlit as st
from utils.api import get_binance_pairs, get_binance_offers
import pandas as pd
import plotly.graph_objects as go

TRADE_TYPE_COL = 'trade_type'

def calculate_spread(offers_df):
    if offers_df.empty or TRADE_TYPE_COL not in offers_df.columns:
        return None, None

    buy_offers = offers_df[offers_df[TRADE_TYPE_COL] == 'BUY'].sort_values(by='price', ascending=False)
    sell_offers = offers_df[offers_df[TRADE_TYPE_COL] == 'SELL'].sort_values(by='price', ascending=True)

    best_buy_price = buy_offers['price'].iloc[0] if not buy_offers.empty else None
    best_sell_price = sell_offers['price'].iloc[0] if not sell_offers.empty else None

    if best_buy_price and best_sell_price:
        spread = best_sell_price - best_buy_price
        spread_percent = (spread / best_buy_price) * 100 if best_buy_price != 0 else None
        return spread, spread_percent
    return None, None

def display_separator():
    st.markdown("--- ")

def calculate_weighted_average(offers_df, trade_type):
    if offers_df.empty or TRADE_TYPE_COL not in offers_df.columns:
        return None

    filtered_offers = offers_df[offers_df[TRADE_TYPE_COL] == trade_type].copy() # Use .copy() to avoid SettingWithCopyWarning
    if filtered_offers.empty:
        return None
    
    # Ensure 'price' and 'tradableQuantity' are numeric
    if 'price' not in filtered_offers.columns or 'available' not in filtered_offers.columns:
        st.warning("Missing 'price' or 'available' column in offers data.")
        return None
    filtered_offers['price'] = pd.to_numeric(filtered_offers['price'], errors='coerce')
    filtered_offers['available'] = pd.to_numeric(filtered_offers['available'], errors='coerce')
    
    # Drop rows where conversion failed
    filtered_offers.dropna(subset=['price', 'available'], inplace=True)

    if filtered_offers['available'].sum() == 0:
        return None
    
    weighted_average = (filtered_offers['price'] * filtered_offers['available']).sum() / filtered_offers['available'].sum()
    return weighted_average

st.set_page_config(layout="wide", page_title="P2P Dashboard", page_icon="📊")

# --- Session State Initialization ---
# This ensures that our data persists across user interactions (reruns).
if 'offers_df' not in st.session_state:
    st.session_state.offers_df = None

st.title("P2P Dashboard - Educational & Commercial Prototype")

st.write("Welcome to the P2P Dashboard. This application is designed to provide insights into the P2P market, serving as an educational, analytical, and commercial tool.")

display_separator()

st.subheader("Intelligent Filters")

pairs_data = get_binance_pairs()

if pairs_data:
    fiats = sorted(list(set(p['fiat'] for p in pairs_data)))
    cryptos = sorted(list(set(p['asset'] for p in pairs_data)))
    trade_types = sorted(list(set(p['tradeType'] for p in pairs_data)))

    col1, col2, col3 = st.columns(3)

    with col1:
        selected_fiat = st.selectbox("Select Fiat Currency", fiats)
    with col2:
        selected_crypto = st.selectbox("Select Crypto Currency", cryptos)
    with col3:
        selected_trade_type = st.selectbox("Select Trade Type", trade_types)

    if st.button("Fetch Offers", use_container_width=True):
        with st.spinner("Fetching offers..."):
            offers = get_binance_offers(selected_fiat, selected_crypto, selected_trade_type)
            if offers:
                # Store the fetched data in the session state
                st.session_state.offers_df = pd.DataFrame(offers)
            else:
                st.session_state.offers_df = None # Clear previous results if no new offers are found
                st.warning("No offers found for the selected criteria. Please try different filters.")

    # --- Display Area ---
    # This part of the code will now run on every interaction,
    # and it will use the data stored in the session state.
    if st.session_state.offers_df is not None:
        df = st.session_state.offers_df
        st.subheader("Available Offers")
        st.dataframe(df)

        display_separator()
        st.subheader("Financial Charts")

        # Calculate and display spread
        spread, spread_percent = calculate_spread(df)
        if spread is not None and spread_percent is not None:
            st.write(f"**Absolute Spread:** {spread:.2f} {selected_fiat}")
            st.write(f"**Relative Spread:** {spread_percent:.2f}%")
        else:
            st.info("Could not calculate spread (insufficient buy/sell offers).")

        # Market Depth Chart
        st.markdown("**Market Depth**")
        buy_orders = df[df[TRADE_TYPE_COL] == 'BUY'].sort_values(by='price', ascending=False)
        sell_orders = df[df[TRADE_TYPE_COL] == 'SELL'].sort_values(by='price', ascending=True)

        # Calculate cumulative volume for buy orders
        buy_orders['cumulative_amount'] = buy_orders['available'].cumsum()
        # Calculate cumulative volume for sell orders
        sell_orders['cumulative_amount'] = sell_orders['available'].cumsum()

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=buy_orders['cumulative_amount'], y=buy_orders['price'],
                                    mode='lines', name='Buy Orders', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=sell_orders['cumulative_amount'], y=sell_orders['price'],
                                    mode='lines', name='Sell Orders', line=dict(color='red')))

        fig.update_layout(title='Market Depth',
                            xaxis_title='Cumulative Amount',
                            yaxis_title='Price',
                            hovermode='x unified')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("**Accumulated Liquidity Curve**")
        # Accumulated Liquidity Curve
        # Assuming 'available' is the volume and 'price' is the price
        # For buy orders, liquidity accumulates as price decreases
        buy_liquidity = buy_orders.sort_values(by='price', ascending=False)
        buy_liquidity['cumulative_volume'] = buy_liquidity['available'].cumsum()

        # For sell orders, liquidity accumulates as price increases
        sell_liquidity = sell_orders.sort_values(by='price', ascending=True)
        sell_liquidity['cumulative_volume'] = sell_liquidity['available'].cumsum()

        fig_liquidity = go.Figure()
        fig_liquidity.add_trace(go.Scatter(x=buy_liquidity['price'], y=buy_liquidity['cumulative_volume'],
                                            mode='lines', name='Buy Liquidity', line=dict(color='green')))
        fig_liquidity.add_trace(go.Scatter(x=sell_liquidity['price'], y=sell_liquidity['cumulative_volume'],
                                            mode='lines', name='Sell Liquidity', line=dict(color='red')))

        fig_liquidity.update_layout(title='Accumulated Liquidity Curve',
                                    xaxis_title='Price',
                                    yaxis_title='Cumulative Volume',
                                    hovermode='x unified')
        st.plotly_chart(fig_liquidity, use_container_width=True)
        st.markdown("**Local Volatility per Pair:** [Coming Soon]")

        # Weighted Average
        weighted_avg_buy = calculate_weighted_average(df, 'BUY')
        weighted_avg_sell = calculate_weighted_average(df, 'SELL')

        if weighted_avg_buy is not None:
            st.write(f"**Weighted Average Buy Price:** {weighted_avg_buy:.2f} {selected_fiat}")
        if weighted_avg_sell is not None:
            st.write(f"**Weighted Average Sell Price:** {weighted_avg_sell:.2f} {selected_fiat}")

        display_separator()
        st.subheader("Analytical Perspectives")
        st.write("This section offers different analytical views of the P2P market, tailored for various audiences.")

        with st.expander("👁️ Market View: Volume, Extreme Prices, Top Merchants"):
            st.write("**Market Overview:** This view provides a snapshot of the current market, highlighting key metrics like total volume, extreme prices (highest buy, lowest sell), and identifying top merchants based on their activity or reputation (if available).")
            st.markdown("**Key Metrics:**")
            st.markdown(f"- **Total Offers:** {len(df)}")
            if not df.empty:
                st.markdown(f"- **Highest Buy Price:** {df[df[TRADE_TYPE_COL] == 'BUY']['price'].max():.2f} {selected_fiat}")
                st.markdown(f"- **Lowest Sell Price:** {df[df[TRADE_TYPE_COL] == 'SELL']['price'].min():.2f} {selected_fiat}")
            st.markdown("**Top Merchants:** [Coming Soon - Requires merchant data]")

        with st.expander("🎓 Educational View: Step-by-Step Explanation"):
            st.write("**Understanding P2P Trading:** This section is designed to educate users about the P2P market. It provides step-by-step explanations of concepts like order books, liquidity, and how prices are formed.")
            st.markdown("**Key Concepts:**")
            st.markdown("- **Order Book:** Visual representation of buy and sell orders.")
            st.markdown("- **Spread:** The difference between the best buy and sell prices.")
            st.markdown("- **Liquidity:** The ease with which an asset can be converted into cash without affecting its market price.")

        with st.expander("💼 Stakeholder View: Storytelling + Key KPIs"):
            st.write("**Project Overview for Stakeholders:** This view presents the project's value proposition, key performance indicators (KPIs), and future vision in a clear and concise manner, suitable for business presentations.")
            st.markdown("**Value Proposition:** [Summarize the core value of the platform]")
            st.markdown("**Key Performance Indicators (KPIs):**")
            st.markdown("- **User Engagement:** [Data Placeholder]")
            st.markdown("- **Transaction Volume:** [Data Placeholder]")
            st.markdown("- **Market Coverage:** [Data Placeholder]")
            st.markdown("**Roadmap & Future Vision:** [Outline future plans and scalability]")

        with st.expander("📊 Comparative View: Multiple Pairs in Parallel"):
            st.write("**Compare P2P Pairs:** This view allows for a side-by-side comparison of different P2P trading pairs, enabling users to identify arbitrage opportunities or analyze market dynamics across various cryptocurrencies or fiat currencies.")
            st.markdown("**Comparison Features:** [Coming Soon - Requires multi-pair data fetching]")

        display_separator()
        st.subheader("Notes and Feedback Panel")
        st.write("Use this panel to take notes or provide feedback.")

        notes_content = st.text_area("Your Notes", "Type your notes here...", height=200)
        
        # Export notes to .txt
        st.download_button(
            label="Export Notes to .txt",
            data=notes_content,
            file_name="p2p_dashboard_notes.txt",
            mime="text/plain"
        )

        display_separator()
        st.subheader("📘 Educational Documentation")

        st.markdown("**Glosario en línea (expandible)**")
        with st.expander("Glosario de Términos P2P"):
            st.markdown("**P2P (Peer-to-Peer):** Transacciones directas entre usuarios sin intermediarios.")
            st.markdown("**Fiat:** Moneda emitida por un gobierno (ej. USD, EUR, ARS).")
            st.markdown("**Crypto:** Criptomoneda (ej. BTC, USDT, ETH).")
            st.markdown("**Spread:** La diferencia entre el mejor precio de compra y el mejor precio de venta.")
            st.markdown("**Liquidez:** La facilidad con la que un activo puede ser comprado o vendido sin afectar su precio.")
            st.markdown("**Orden de Compra/Venta:** Una solicitud para comprar o vender una cantidad específica de cripto a un precio determinado.")
            st.markdown("**Volumen de Trading:** La cantidad total de un activo que se ha negociado en un período determinado.")

        st.markdown("**Tooltip en cada métrica financiera**")
        st.info("Tooltips are integrated directly into the relevant metrics and charts above (e.g., hover over chart elements).")

        st.markdown("**Botón “¿Qué significa esto?” para spreads, límites, etc.**")
        with st.expander("¿Qué significa el Spread?"):
            st.markdown("El **Spread** es la diferencia entre el precio más alto que un comprador está dispuesto a pagar (oferta de compra) y el precio más bajo que un vendedor está dispuesto a aceptar (oferta de venta). Un spread pequeño indica un mercado líquido y eficiente, mientras que un spread grande puede sugerir baja liquidez o mayor volatilidad.")

        with st.expander("¿Qué significan los Límites de Trading?"):
            st.markdown("Los **Límites de Trading** se refieren a la cantidad mínima y máxima de criptomoneda que un comerciante está dispuesto a comprar o vender en una sola transacción. Estos límites son establecidos por el comerciante y pueden variar ampliamente.")

        st.markdown("**Diagrama visual de arquitectura**")
        st.info("**[Diagrama de Arquitectura - Placeholder]** Un diagrama visual que ilustra la interacción entre el frontend Streamlit, el backend FastAPI y las fuentes de datos (Binance, Bybit) se incluirá aquí.")

else:
    st.error("Could not fetch available pairs from the backend. Please ensure the FastAPI backend is running.")

display_separator()
