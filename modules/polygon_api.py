import requests
import pandas as pd
import streamlit as st

# Try to get API key from secrets, fallback to demo if not found
try:
    API_KEY = st.secrets["POLYGON_API_KEY"]
except (KeyError, FileNotFoundError):
    API_KEY = "DEMO_API_KEY"
    st.warning("⚠️ Using demo API key. Please add your Polygon.io API key to .streamlit/secrets.toml")

BASE_URL = "https://api.polygon.io"

def fetch_financials(ticker):
    """Fetch financial statements from Polygon.io."""
    url = f"{BASE_URL}/v2/reference/financials/{ticker}?apiKey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('status') == 'OK':
            financials = data.get('results', [])
            income_df = pd.DataFrame([{
                'revenues': f.get('financials', {}).get('income_statement', {}).get('revenues', 0),
                'operating_expenses': f.get('financials', {}).get('income_statement', {}).get('operating_expenses', 0),
                'net_income': f.get('financials', {}).get('income_statement', {}).get('net_income_loss', 0)
            } for f in financials])
            balance_df = pd.DataFrame([{
                'total_assets': f.get('financials', {}).get('balance_sheet', {}).get('total_assets', 0),
                'total_liabilities': f.get('financials', {}).get('balance_sheet', {}).get('total_liabilities', 0),
                'total_equity': f.get('financials', {}).get('balance_sheet', {}).get('total_equity', 0)
            } for f in financials])
            return {'income': income_df, 'balance': balance_df}
    except Exception as e:
        st.error(f"Error fetching financials: {str(e)}")
    return {'income': pd.DataFrame(), 'balance': pd.DataFrame()}

def fetch_company_info(ticker):
    """Fetch company information from Polygon.io."""
    url = f"{BASE_URL}/v3/reference/tickers/{ticker}?apiKey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('status') == 'OK':
            results = data.get('results', {})
            return {
                'name': results.get('name'),
                'market_cap': results.get('market_cap'),
                'description': results.get('description')
            }
    except Exception as e:
        st.error(f"Error fetching company info: {str(e)}")
    return {}

def fetch_market_data(ticker):
    """Fetch current market data from Polygon.io."""
    url = f"{BASE_URL}/v2/snapshot/locale/us/markets/stocks/tickers/{ticker}?apiKey={API_KEY}"
    try:
        response = requests.get(url)
        data = response.json()
        if data.get('status') == 'OK':
            ticker_data = data.get('ticker', {})
            return {
                'price': ticker_data.get('lastTrade', {}).get('p'),
                'volume': ticker_data.get('day', {}).get('v'),
                'market_cap': ticker_data.get('market_cap')
            }
    except Exception as e:
        st.error(f"Error fetching market data: {str(e)}")
    return {}

def fetch_all(ticker):
    """Fetch all relevant data for a given ticker."""
    if API_KEY == "DEMO_API_KEY":
        st.warning("Using demo data since no API key is provided")
        # Return sample data for demo purposes
        return {
            'financials': {
                'income': pd.DataFrame({
                    'revenues': [100000000],
                    'operating_expenses': [70000000],
                    'net_income': [20000000]
                }),
                'balance': pd.DataFrame({
                    'total_assets': [500000000],
                    'total_liabilities': [300000000],
                    'total_equity': [200000000]
                })
            },
            'company_info': {
                'name': 'Demo Company',
                'market_cap': 1000000000,
                'description': 'This is demo data. Please add your Polygon.io API key to use real data.'
            },
            'market_data': {
                'price': 100,
                'volume': 1000000,
                'market_cap': 1000000000
            },
            'market_cap_ev': {
                'market_cap': 1000000000,
                'enterprise_value': 1200000000
            }
        }
    
    return {
        'financials': fetch_financials(ticker),
        'company_info': fetch_company_info(ticker),
        'market_data': fetch_market_data(ticker),
        'market_cap_ev': {
            'market_cap': fetch_market_data(ticker).get('market_cap', 0),
            'enterprise_value': None  # Would need additional calculation
        }
    } 