import pytest
import requests
import os
from unittest.mock import Mock, patch
import streamlit as st

# Assuming utils/api.py is structured such that BASE_URL and functions are importable
# For testing, we might need to adjust the import path or mock os.getenv

# Mock the os.getenv for P2P_DASHBOARD_API_KEY
@pytest.fixture(autouse=True)
def mock_env_vars():
    with patch.dict(os.environ, {"P2P_DASHBOARD_API_KEY": "test_api_key"}):
        yield

# Mock st.session_state for tests
@pytest.fixture(autouse=True)
def mock_st_session_state():
    with patch.object(st, "session_state", {}):
        yield

# Mock st.error for tests
@pytest.fixture(autouse=True)
def mock_st_error():
    with patch.object(st, "error") as mock_error:
        yield mock_error

# Mock st.cache_data to prevent actual caching during tests
@pytest.fixture(autouse=True)
def mock_st_cache_data():
    with patch.object(st, "cache_data", lambda func=None, **kwargs: func) as mock_cache:
        yield mock_cache

# Import api after mocking Streamlit components
from streamlit_app.utils import api


def test_get_headers_from_env(mock_st_session_state):
    """Test that headers are correctly formed from environment variable."""
    headers = api._get_headers()
    assert headers == {"X-API-Key": "test_api_key"}


def test_get_headers_from_session_state(mock_st_session_state):
    """Test that headers are correctly formed from session state if env var is not set."""
    del os.environ["P2P_DASHBOARD_API_KEY"]
    st.session_state['api_key'] = "session_api_key"
    headers = api._get_headers()
    assert headers == {"X-API-Key": "session_api_key"}


def test_get_headers_no_api_key(mock_st_session_state, mock_st_error):
    """Test that _get_headers returns None and shows error if no API key is found."""
    del os.environ["P2P_DASHBOARD_API_KEY"]
    if 'api_key' in st.session_state:
        del st.session_state['api_key']
    headers = api._get_headers()
    assert headers is None
    mock_st_error.assert_called_once_with("API Key not found. Please set the P2P_DASHBOARD_API_KEY environment variable.")


@patch('requests.get')
def test_get_binance_pairs_success(mock_get, mock_st_session_state):
    """Test successful fetching of Binance pairs."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"fiat": "USD", "asset": "USDT"}]
    mock_get.return_value = mock_response

    pairs = api.get_binance_pairs()
    assert pairs == [{"fiat": "USD", "asset": "USDT"}]
    mock_get.assert_called_once_with(f"{api.BASE_URL}/api/v1/binance/pairs", headers=api._get_headers())


@patch('requests.get')
def test_get_binance_pairs_api_error(mock_get, mock_st_session_state, mock_st_error):
    """Test error handling when fetching Binance pairs fails."""
    api.get_binance_pairs.clear()
    mock_get.side_effect = requests.exceptions.RequestException("Test API Error")

    pairs = api.get_binance_pairs()
    assert pairs == []
    mock_st_error.assert_called_once_with("Error fetching Binance pairs: Test API Error")


@patch('requests.get')
def test_get_binance_offers_success(mock_get, mock_st_session_state):
    """Test successful fetching of Binance offers."""
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = [{"price": "1.0", "available": "100"}]
    mock_get.return_value = mock_response

    offers = api.get_binance_offers("USD", "USDT", "BUY")
    assert offers == [{"price": "1.0", "available": "100"}]
    mock_get.assert_called_once_with(
        f"{api.BASE_URL}/api/v1/binance/offers",
        headers=api._get_headers(),
        params={
            "fiat": "USD",
            "asset": "USDT",
            "trade_type": "BUY"
        }
    )


@patch('requests.get')
def test_get_binance_offers_api_error(mock_get, mock_st_session_state, mock_st_error):
    """Test error handling when fetching Binance offers fails."""
    api.get_binance_offers.clear()
    mock_get.side_effect = requests.exceptions.RequestException("Test API Error")

    offers = api.get_binance_offers("USD", "USDT", "BUY")
    assert offers == []
    mock_st_error.assert_called_once_with("Error fetching Binance offers: Test API Error")


@patch('requests.get')
def test_get_bybit_offers_api_error(mock_get, mock_st_session_state, mock_st_error):
    """Test error handling when fetching Bybit offers fails."""
    api.get_bybit_offers.clear()
    mock_get.side_effect = requests.exceptions.RequestException("Test API Error")

    offers = api.get_bybit_offers("USD", "USDT", "1")
    assert offers == []
    mock_st_error.assert_called_once_with("Error fetching Bybit offers: Test API Error")
