
# Product Requirements Document (PRD) for P2P Dashboard Streamlit Frontend

## 1. Overview

This document outlines the requirements for building an **outstanding, dark-mode-enabled Streamlit web application** that serves as a sophisticated frontend for the P2P Dashboard API. The application will empower users to interactively explore and visualize P2P cryptocurrency offers from various exchanges, initially focusing on Binance and Bybit.

The primary goal is to create a visually stunning, highly intuitive, and performant interface that provides clear, real-time data with an emphasis on exceptional data interaction and visualization, reflecting the expertise of a data scientist. The presentation of information will be a key differentiator, designed to be both informative and aesthetically pleasing.

## 2. Target Audience

The target audience for this application includes:

*   **Cryptocurrency Traders:** Individuals who actively participate in P2P trading and require a comprehensive, visually engaging dashboard to monitor offers across different platforms.
*   **Arbitrageurs:** Traders seeking price discrepancies between exchanges, who will benefit from clear, comparative data visualization.
*   **Data Analysts:** Individuals interested in analyzing P2P market data for research, trend analysis, and pattern identification, presented in an accessible and interactive format.

## 3. Key Features

The Streamlit application will offer the following core features, designed for optimal user experience and data insight:

*   **API Key Management:** Secure input and session-based storage of API keys for seamless access to the backend API.
*   **Multi-Exchange Data Aggregation:** Users can effortlessly switch between and view aggregated offers from supported exchanges (Binance, Bybit).
*   **Dynamic Pair Discovery & Filtering:** Intelligent fetching and display of available trading pairs, coupled with robust filtering options:
    *   **Fiat Currency:** (e.g., USD, EUR, NGN)
    *   **Cryptocurrency Asset:** (e.g., USDT, BTC, ETH)
    *   **Trade Type:** (Buy or Sell)
*   **Interactive Offer Display:** A highly customizable and interactive table (`st.dataframe` with enhanced styling) of P2P offers, featuring:
    *   Sortable columns: Price, Available Quantity, Min/Max Trade Limits.
    *   Clear display of Payment Methods and Advertiser details (Name, Rating).
    *   Conditional formatting to highlight key metrics (e.g., best prices).
*   **Visual Data Summaries:** Concise, impactful visualizations (e.g., bar charts for price distribution, pie charts for payment method prevalence) to provide quick insights into market dynamics.

## 4. API Endpoints and Interaction

The Streamlit application will seamlessly interact with the P2P Dashboard API, ensuring secure and efficient data retrieval. All API calls will be managed by a dedicated utility module (`utils/api.py`) to centralize logic and enhance maintainability.

### 4.1. Authentication

All requests to the API must include a valid API key in the `X-API-Key` header. The Streamlit application will prompt the user for their API key upon first access or if the key is invalid/missing. This key will be securely stored in Streamlit's session state (`st.session_state`) and used for all subsequent API calls, never exposed in the UI.

*   **Header:** `X-API-Key: <YOUR_API_KEY>`

### 4.2. Binance Endpoints

*   **Get Available Pairs:**
    *   **Endpoint:** `/api/v1/binance/pairs`
    *   **Method:** `GET`
    *   **Description:** Retrieves a list of all available trading pairs on Binance P2P.
*   **Get P2P Offers:**
    *   **Endpoint:** `/api/v1/binance/offers`
    *   **Method:** `GET`
    *   **Description:** Retrieves P2P offers for a specific trading pair and trade type.
    *   **Query Parameters:** `fiat`, `asset`, `trade_type`

### 4.3. Bybit Endpoints

*   **Get P2P Offers:**
    *   **Endpoint:** `/api/v1/bybit/offers`
    *   **Method:** `GET`
    *   **Description:** Retrieves P2P offers from Bybit.
    *   **Query Parameters:** `currency`, `token`, `side`

## 5. User Interface (UI) and User Experience (UX) - The "A+" Dashboard

The UI/UX will be the cornerstone of this application, designed for clarity, elegance, and powerful data interaction.

*   **Theme & Aesthetics:**
    *   **Dark Mode First:** The application will default to a sophisticated dark theme, utilizing deep, rich background colors (e.g., `#1a1a2e`, `#0f0f2c`).
    *   **Color Palette:** Accent colors will be carefully chosen to provide contrast and highlight key information without being overwhelming. A palette of cool blues (`#00bcd4`, `#007bff`), vibrant greens (`#28a745`), and subtle purples (`#6f42c1`) will be used for interactive elements, charts, and data highlights.
    *   **Typography:** Modern, clean sans-serif fonts (e.g., 'Inter', 'Roboto', 'Open Sans') will be used for readability and a professional feel.
    *   **Custom CSS:** Strategic use of custom CSS (`st.markdown('<style>...</style>', unsafe_allow_html=True)`) to fine-tune spacing, component styling, and ensure a cohesive visual identity.

*   **Layout & Navigation:**
    *   **Main Layout:** A clean, multi-column layout using `st.columns` and `st.container` to logically group related controls and data displays.
    *   **Sidebar (`st.sidebar`):** Dedicated for global controls such as API Key input, Exchange Selection, and potentially a "Dashboard Overview" or "Settings" link.
    *   **Tabbed Interface (`st.tabs`):** The primary content area will utilize tabs for distinct views, allowing users to easily switch between:
        *   **"Binance P2P Offers":** Dedicated view for Binance data.
        *   **"Bybit P2P Offers":** Dedicated view for Bybit data.
        *   **"Arbitrage Opportunities":** (Future enhancement, but planned for layout) A comparative view highlighting potential arbitrage.
        *   **"Market Insights":** (Future enhancement) Visualizations and summaries.
    *   **Expanders (`st.expander`):** Used within tabs for collapsible sections, such as detailed filtering options or advanced data views, to maintain a clean initial interface.

*   **Data Presentation & Interaction:**
    *   **Interactive DataFrames:** `st.dataframe` will be styled for dark mode, with clear headers, row highlighting on hover, and intuitive sorting.
    *   **Key Performance Indicators (KPIs):** Prominent display of aggregated metrics (e.g., "Lowest Price USDT/USD Binance Buy") using `st.metric` or custom styled cards.
    *   **Visualizations:**
        *   **Price Distribution:** Histograms or density plots of offer prices for selected pairs.
        *   **Payment Method Breakdown:** Bar charts or pie charts showing the distribution of payment methods.
        *   **Advertiser Ratings:** Visual representation of advertiser reputation.
    *   **Real-time Feedback:** Loading spinners (`st.spinner`), success/error messages (`st.success`, `st.error`), and clear status updates to inform the user about data fetching and processing.

*   **Responsiveness:** The application will be designed to be fully responsive, adapting gracefully to various screen sizes (desktop, tablet, mobile) using Streamlit's inherent responsiveness and careful layout choices.

## 6. Non-Functional Requirements

*   **Performance:** Aggressive caching strategies (`st.cache_data`, `st.cache_resource`) will be employed to minimize API calls and ensure rapid data loading and UI responsiveness. Asynchronous API calls will be explored for improved concurrency.
*   **Security:** API keys will be handled with utmost care, stored only in session state and never persisted or exposed client-side. All communication with the backend API will be over HTTPS.
*   **Maintainability:** The codebase will adhere to Python best practices, with clear module separation (e.g., `utils/api.py` for API interactions, `components/` for reusable UI elements), comprehensive comments, and type hints.
*   **Scalability:** The architecture is designed to easily integrate additional exchanges and features without significant refactoring.

## 7. Future Enhancements

*   **Additional Exchanges:** Seamless integration with other major P2P exchanges (e.g., KuCoin, OKX) to expand data coverage.
*   **Advanced Data Visualization:** Interactive charts for historical price trends, volume analysis, and more sophisticated market insights.
*   **User Accounts & Preferences:** Implementation of a user authentication system to save API keys, preferred settings, and custom alerts.
*   **Real-time Updates & Alerts:** Automatic refreshing of offer data at configurable intervals and push notifications for price changes or new opportunities.
*   **Arbitrage Calculator:** A dedicated tool to calculate potential profits from arbitrage opportunities across exchanges.
