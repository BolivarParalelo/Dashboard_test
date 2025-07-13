# P2P Cryptocurrency Offer Dashboard

![Dashboard Screenshot](https://via.placeholder.com/800x400?text=P2P+Dashboard+Screenshot) <!-- Placeholder for a future screenshot -->

## Overview

This is an **outstanding, dark-mode-enabled Streamlit web application** designed to provide a sophisticated and intuitive interface for exploring and visualizing P2P (Peer-to-Peer) cryptocurrency offers from various exchanges. Initially focusing on Binance and Bybit, this dashboard aims to deliver real-time, actionable insights with an emphasis on exceptional data interaction and visualization.

Built with data scientists and active traders in mind, the application prioritizes a clean, modern aesthetic and a highly responsive user experience, making complex market data easily digestible.

## Features

*   **Dark Mode First:** A sleek, sophisticated dark theme for comfortable viewing.
*   **API Key Management:** Secure handling of API keys for seamless backend integration.
*   **Multi-Exchange Data Aggregation:** View and compare P2P offers from Binance and Bybit.
*   **Dynamic Filtering:** Filter offers by fiat currency (e.g., USD, NGN, EUR), cryptocurrency asset (e.g., USDT, BTC, ETH), and trade type (Buy/Sell).
*   **Interactive Offer Display:** Sortable and filterable tables (`st.dataframe`) with key offer details.
*   **Manual Cache Refresh:** Buttons to explicitly clear data cache and fetch the latest offers, ensuring data freshness.
*   **Responsive Design:** Adapts gracefully to various screen sizes.

## Getting Started

### Prerequisites

Before running the dashboard, ensure you have:

*   **Python 3.8+** installed.
*   **Access to the P2P Dashboard API Backend:** This frontend application relies on a separate FastAPI backend. Ensure your backend is running and accessible.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/BolivarParalelo/Dashboard_test.git
    cd Dashboard_test/streamlit_app
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure your API Key:**
    Create a `.env` file in the `streamlit_app/` directory (the same directory as `app.py`).
    ```
    # streamlit_app/.env
    P2P_DASHBOARD_API_KEY="YOUR_ACTUAL_BACKEND_API_KEY_HERE"
    ```
    Replace `YOUR_ACTUAL_BACKEND_API_KEY_HERE` with the API key required by your P2P Dashboard API backend.
    
    *Note: The `.env` file is automatically ignored by Git to protect your sensitive information.*

### Running the Application

Navigate to the `streamlit_app/` directory in your terminal and run:

```bash
streamlit run app.py
```

The application will open in your web browser (usually `http://localhost:8501`).

## Usage

1.  **Select Exchange:** Use the sidebar to choose between Binance and Bybit.
2.  **Apply Filters:** Select your desired Fiat Currency, Crypto Asset, and Trade Type.
3.  **Fetch Offers:** Click the "Fetch Offers" button to retrieve data based on your criteria.
4.  **Refresh Data:** Use the "Refresh Offers" button to clear the cache and get the latest data from the API.

## API Backend

This Streamlit application interacts with a dedicated P2P Dashboard API backend. This intermediary API provides a unified, secure, and performant way to access and process data from various P2P exchanges. For more details on the backend's purpose and architecture, refer to `why_this_app.md`.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is open-source and available under the [MIT License](LICENSE). <!-- Assuming MIT License, create a LICENSE file if not present -->

## Contact

For questions or feedback, please open an issue on the GitHub repository.