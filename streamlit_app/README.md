# P2P Dashboard Streamlit Application

This directory contains the Streamlit frontend application for the P2P Dashboard, designed to provide an educational, analytical, and commercial interface to the FastAPI backend.

## Features

- **Intelligent Filters:** Filter P2P offers by fiat currency, cryptocurrency, and trade type.
- **Offer Visualization:** View P2P offers in a clean, sortable table.
- **Financial Charts:** Visualize market depth, accumulated liquidity, and calculated spreads.
- **Analytical Perspectives:** Explore different views of the market for various audiences (Market, Educational, Stakeholder, Comparative).
- **Notes and Feedback:** A panel to take notes and export them.
- **Educational Documentation:** Glossary of P2P terms and explanations of key financial metrics.

## Setup and Running

To set up and run this Streamlit application, follow these steps:

1.  **Navigate to the `streamlit_app` directory:**
    ```bash
    cd C:/Users/DELL/P2P-Dashboard/streamlit_app
    ```

2.  **Create a new virtual environment (recommended):**
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment:**
    *   On Windows:
        ```bash
        .\venv\Scripts\activate
        ```
    *   On macOS/Linux:
        ```bash
        source venv/bin/activate
        ```

4.  **Install the required packages:**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Run the FastAPI backend (if not already running):**
    *   Open a new terminal and navigate to the `C:/Users/DELL/P2P-Dashboard/` directory.
    *   Run:
        ```bash
        uvicorn p2p_api.main:app --reload
        ```
    *   This will typically run on `http://127.0.0.1:8000`.

6.  **Run the Streamlit application:**
    *   In the terminal where you activated the `streamlit_app` virtual environment, run:
        ```bash
        streamlit run app.py
        ```
    *   This will open the Streamlit app in your web browser, typically on `http://localhost:8501`.

## Project Structure

```
streamlit_app/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies for the Streamlit app
├── utils/
│   └── api.py             # Module for interacting with the FastAPI backend
└── docs/
    └── README.md          # Documentation for the Streamlit app
```
