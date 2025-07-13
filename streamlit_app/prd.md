
# Product Requirements Document (PRD) for P2P Dashboard Streamlit Frontend

## 1. Overview

This document outlines the requirements for building a Streamlit web application that serves as a frontend for the P2P Dashboard API. The application will allow users to view P2P cryptocurrency offers from various exchanges, starting with Binance and Bybit.

The primary goal is to create a user-friendly interface that is easy to navigate and provides clear, real-time data. The application will be built using Streamlit, a Python library for creating web apps for data science and machine learning.

## 2. Target Audience

The target audience for this application includes:

*   **Cryptocurrency Traders:** Individuals who actively participate in P2P trading and need a comprehensive dashboard to monitor offers across different platforms.
*   **Arbitrageurs:** Traders looking for price discrepancies between exchanges to make a profit.
*   **Data Analysts:** Individuals interested in analyzing P2P market data for research or trend analysis.

## 3. Key Features

The Streamlit application will have the following key features:

*   **API Key Authentication:** Users must provide a valid API key to access the application's features.
*   **Exchange Selection:** Users can select the exchange (Binance or Bybit) from which they want to view offers.
*   **Pair Discovery:** The application will dynamically fetch and display the available trading pairs for the selected exchange.
*   **Offer Filtering:** Users can filter offers based on:
    *   **Fiat Currency:** (e.g., USD, EUR, NGN)
    *   **Cryptocurrency Asset:** (e.g., USDT, BTC, ETH)
    *   **Trade Type:** (Buy or Sell)
*   **Offer Display:** The application will display a sortable and filterable table of P2P offers with the following information:
    *   Price
    *   Available Quantity
    *   Minimum and Maximum Trade Limits
    *   Payment Methods
    *   Advertiser's Name and Rating

## 4. API Endpoints and Interaction

The Streamlit application will interact with the following API endpoints provided by the P2P Dashboard API:

### 4.1. Authentication

All requests to the API must include a valid API key in the `X-API-Key` header.

*   **Header:** `X-API-Key: <YOUR_API_KEY>`

The Streamlit application should prompt the user to enter their API key, which will then be used for all subsequent API calls. The key should be stored securely in the application's session state and not exposed in the UI.

### 4.2. Binance Endpoints

*   **Get Available Pairs:**
    *   **Endpoint:** `/api/v1/binance/pairs`
    *   **Method:** `GET`
    *   **Description:** Retrieves a list of all available trading pairs on Binance P2P.
    *   **Successful Response (200 OK):**
        ```json
        [
          {
            "fiat": "USD",
            "asset": "USDT"
          },
          {
            "fiat": "EUR",
            "asset": "BTC"
          }
        ]
        ```

*   **Get P2P Offers:**
    *   **Endpoint:** `/api/v1/binance/offers`
    *   **Method:** `GET`
    *   **Description:** Retrieves P2P offers for a specific trading pair and trade type.
    *   **Query Parameters:**
        *   `fiat` (string, required): The fiat currency (e.g., "USD").
        *   `asset` (string, required): The cryptocurrency asset (e.g., "USDT").
        *   `trade_type` (string, required): "BUY" or "SELL".
    *   **Successful Response (200 OK):**
        ```json
        [
          {
            "price": "0.99",
            "available": "1000.00",
            "min_limit": "10.00",
            "max_limit": "500.00",
            "payment_methods": ["Bank Transfer", "Wise"],
            "advertiser": "TraderPro"
          }
        ]
        ```

### 4.3. Bybit Endpoints

*   **Get P2P Offers:**
    *   **Endpoint:** `/api/v1/bybit/offers`
    *   **Method:** `GET`
    *   **Description:** Retrieves P2P offers from Bybit.
    *   **Query Parameters:**
        *   `currency` (string, required): The fiat currency (e.g., "USD").
        *   `token` (string, required): The cryptocurrency asset (e.g., "USDT").
        *   `side` (string, required): "1" for Buy, "0" for Sell.
    *   **Successful Response (200 OK):**
        ```json
        [
          {
            "price": "1.01",
            "available": "500.00",
            "min_limit": "20.00",
            "max_limit": "200.00",
            "payment_methods": ["Advcash"],
            "advertiser": "CryptoKing"
          }
        ]
        ```

## 5. User Interface (UI) and User Experience (UX)

*   **Layout:** The application should have a clean and intuitive layout. A sidebar can be used for API key input, exchange selection, and filtering options.
*   **Data Display:** The offer data should be presented in a `st.dataframe` or a similar interactive table.
*   **Error Handling:** The application should gracefully handle API errors (e.g., invalid API key, no offers found) and display informative messages to the user.
*   **Responsiveness:** The application should be responsive and usable on different screen sizes.

## 6. Non-Functional Requirements

*   **Performance:** The application should be performant and load data quickly. Caching mechanisms in Streamlit (`st.cache_data`) should be used to avoid redundant API calls.
*   **Security:** The API key should be handled securely and not exposed to the client-side.
*   **Maintainability:** The code should be well-structured, commented, and easy to maintain.

## 7. Future Enhancements

*   **Additional Exchanges:** Integration with other P2P exchanges (e.g., KuCoin, OKX).
*   **Data Visualization:** Charts and graphs to visualize price trends and historical data.
*   **User Accounts:** A system for users to save their API keys and preferences.
*   **Real-time Updates:** Automatic refreshing of offer data.
