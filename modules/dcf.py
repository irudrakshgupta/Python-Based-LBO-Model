import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objs as go
from modules.utils import neon_palette

def project_fcf(financials, rev_growth, ebitda_margin, years=5):
    """Project Free Cash Flow for N years based on user assumptions and historicals."""
    # Use last year as base
    if financials is None or 'income' not in financials or financials['income'].empty:
        return []
    base_revenue = financials['income'].iloc[0]['revenues']
    fcf_list = []
    revenue = base_revenue
    for i in range(years):
        revenue *= (1 + rev_growth / 100)
        ebitda = revenue * (ebitda_margin / 100)
        # Assume FCF = EBITDA * 0.7 (placeholder, to be refined)
        fcf = ebitda * 0.7
        fcf_list.append(fcf)
    return fcf_list

def calculate_terminal_value(last_fcf, method, exit_multiple=None, gordon_growth_rate=None, discount_rate=None):
    """Calculate terminal value using either exit multiple or Gordon Growth method."""
    if method == 'exit_multiple' and exit_multiple:
        return last_fcf * exit_multiple
    elif method == 'gordon_growth' and gordon_growth_rate is not None and discount_rate is not None:
        return last_fcf * (1 + gordon_growth_rate / 100) / (discount_rate / 100 - gordon_growth_rate / 100)
    else:
        return 0

def discount_cash_flows(fcf_list, discount_rate):
    """Discount projected FCFs to present value."""
    discounted = [fcf / ((1 + discount_rate / 100) ** (i + 1)) for i, fcf in enumerate(fcf_list)]
    return discounted

def run(data, rev_growth, ebitda_margin, discount_rate, exit_multiple, exit_year):
    """Run the full DCF model and return all outputs as a dict."""
    financials = data.get('financials', {})
    fcf_list = project_fcf(financials, rev_growth, ebitda_margin, years=exit_year)
    discounted_fcfs = discount_cash_flows(fcf_list, discount_rate)
    terminal_value = calculate_terminal_value(
        fcf_list[-1] if fcf_list else 0,
        method='exit_multiple',
        exit_multiple=exit_multiple
    )
    discounted_terminal = terminal_value / ((1 + discount_rate / 100) ** exit_year)
    enterprise_value = sum(discounted_fcfs) + discounted_terminal
    # Equity value = EV - net debt (placeholder: use market cap if available)
    market_cap_ev = data.get('market_cap_ev', {})
    net_debt = 0
    if market_cap_ev:
        net_debt = (market_cap_ev.get('enterprise_value') or 0) - (market_cap_ev.get('market_cap') or 0)
    equity_value = enterprise_value - net_debt
    fair_value_per_share = None  # Placeholder, needs shares outstanding
    return {
        'fcf_list': fcf_list,
        'discounted_fcfs': discounted_fcfs,
        'terminal_value': terminal_value,
        'discounted_terminal': discounted_terminal,
        'enterprise_value': enterprise_value,
        'equity_value': equity_value,
        'fair_value_per_share': fair_value_per_share,
        'intrinsic_vs_market_gap': None  # Placeholder
    }

def display(outputs):
    """Display DCF results and charts in Streamlit."""
    if not outputs or not outputs.get('fcf_list'):
        st.warning("No DCF results to display.")
        return
    st.subheader("DCF Valuation Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Enterprise Value", f"${outputs['enterprise_value']:,.0f}")
    col2.metric("Equity Value", f"${outputs['equity_value']:,.0f}")
    col3.metric("Terminal Value", f"${outputs['terminal_value']:,.0f}")
    st.subheader("Discounted Cash Flows")
    years = list(range(1, len(outputs['fcf_list']) + 1))
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=years,
        y=outputs['discounted_fcfs'],
        name="Discounted FCF",
        marker_color=neon_palette()[0]
    ))
    fig.add_trace(go.Scatter(
        x=years,
        y=outputs['fcf_list'],
        name="Projected FCF",
        mode="lines+markers",
        line=dict(color=neon_palette()[1], width=3)
    ))
    fig.update_layout(
        template="plotly_dark",
        title="Projected vs Discounted FCF",
        xaxis_title="Year",
        yaxis_title="USD",
        plot_bgcolor="#18181b",
        paper_bgcolor="#18181b",
        font=dict(color="#00ffe7")
    )
    st.plotly_chart(fig, use_container_width=True) 