import streamlit as st
from modules import polygon_api, dcf, lbo, growth_simulator

st.set_page_config(
    page_title="LBO & DCF Valuation Suite",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add custom styling
st.markdown("""
    <style>
    .main {
        background-color: #0E1117;
        color: #00FFE7;
    }
    .stButton>button {
        background-color: #00FFE7;
        color: #0E1117;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #1E1E1E;
        border-radius: 4px 4px 0px 0px;
        padding: 10px 20px;
        color: #00FFE7;
    }
    .stTabs [aria-selected="true"] {
        background-color: #00FFE7 !important;
        color: #0E1117 !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar: Inputs ---
st.sidebar.title("💼 Deal Inputs")
ticker = st.sidebar.text_input("Ticker Symbol", value="AAPL")
if st.sidebar.button("Fetch Data"):
    with st.spinner("Fetching data..."):
        st.session_state['data'] = polygon_api.fetch_all(ticker)
        st.success("Data fetched successfully!")

data = st.session_state.get('data', None)

st.sidebar.subheader("Model Assumptions")
interest_rate = st.sidebar.number_input("Interest Rate (%)", value=5.0)
debt_pct = st.sidebar.slider("% Debt Financing", 0, 100, 60)
exit_year = st.sidebar.number_input("Exit Year", value=5)
exit_multiple = st.sidebar.number_input("Exit Multiple (EBITDA)", value=8.0)
rev_growth = st.sidebar.slider("Revenue Growth Rate (%)", 0, 50, 8)
ebitda_margin = st.sidebar.slider("EBITDA Margin (%)", 0, 100, 22)
discount_rate = st.sidebar.number_input("Discount Rate / WACC (%)", value=10.0)
holding_period = st.sidebar.slider("Holding Period (years)", 1, 10, 5)

# --- Main Tabs ---
tabs = st.tabs([
    "📈 DCF Engine", "💣 LBO Engine", "📊 Growth Simulator", "📅 Debt Forecast"
])

with tabs[0]:
    st.header("📈 DCF Engine")
    if data:
        dcf_outputs = dcf.run(data, rev_growth, ebitda_margin, discount_rate, exit_multiple, exit_year)
        dcf.display(dcf_outputs)
    else:
        st.info("Enter a ticker symbol and fetch data to run DCF model.")

with tabs[1]:
    st.header("💣 LBO Engine")
    if data:
        lbo_outputs = lbo.run(data, debt_pct, interest_rate, exit_multiple, exit_year, holding_period)
        lbo.display(lbo_outputs)
    else:
        st.info("Enter a ticker symbol and fetch data to run LBO model.")

with tabs[2]:
    st.header("📊 Growth Trajectory Simulator")
    growth_simulator.display()

with tabs[3]:
    st.header("📅 Debt Forecast & Payoff")
    if data and 'lbo_outputs' in locals():
        lbo.display_debt_schedule(lbo_outputs)
    else:
        st.info("Run LBO model to view debt schedule.") 