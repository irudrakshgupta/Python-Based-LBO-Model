import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objs as go
from modules.utils import neon_palette, format_currency, format_percentage

def project_ebitda(financials, rev_growth, ebitda_margin, years=5):
    """Project EBITDA for N years based on user assumptions and historicals."""
    if financials is None or 'income' not in financials or financials['income'].empty:
        return []
    base_revenue = financials['income'].iloc[0]['revenues']
    ebitda_list = []
    revenue = base_revenue
    for i in range(years):
        revenue *= (1 + rev_growth / 100)
        ebitda = revenue * (ebitda_margin / 100)
        ebitda_list.append(ebitda)
    return ebitda_list

def model_debt_equity(entry_ebitda, debt_pct, interest_rate, exit_multiple, years):
    """Model debt and equity structure, returns, and payoff schedule."""
    pass

def calculate_irr(cash_flows):
    """Calculate IRR with error handling."""
    try:
        # Add small epsilon to avoid division by zero
        epsilon = 1e-10
        # Use numpy's financial functions
        rate = np.irr(cash_flows)
        if np.isnan(rate) or np.isinf(rate):
            return None
        return rate * 100  # Convert to percentage
    except:
        return None

def calculate_moic(entry_equity, exit_equity):
    """Calculate MOIC (Multiple on Invested Capital)."""
    if entry_equity == 0:
        return None
    return exit_equity / entry_equity

def calculate_dscr(ebitda, debt_service):
    """Calculate Debt Service Coverage Ratio over time."""
    if isinstance(ebitda, list) and isinstance(debt_service, list):
        return [e/d if d else None for e, d in zip(ebitda, debt_service)]
    elif debt_service:
        return ebitda / debt_service
    else:
        return None

def calculate_debt_schedule(purchase_price, debt_pct, interest_rate, years):
    """Calculate debt repayment schedule."""
    initial_debt = purchase_price * (debt_pct / 100)
    annual_payment = initial_debt / years  # Simple straight-line amortization
    
    schedule = []
    remaining_debt = initial_debt
    
    for year in range(years):
        interest = remaining_debt * (interest_rate / 100)
        principal = annual_payment
        total_payment = principal + interest
        remaining_debt -= principal
        
        schedule.append({
            'Year': year + 1,
            'Beginning Balance': remaining_debt + principal,
            'Principal Payment': principal,
            'Interest Payment': interest,
            'Total Payment': total_payment,
            'Ending Balance': remaining_debt
        })
    
    return pd.DataFrame(schedule)

def calculate_returns(purchase_price, exit_value, equity_invested, holding_period, annual_cash_flows=None):
    """Calculate investment returns (IRR, MOIC)."""
    if annual_cash_flows is None:
        annual_cash_flows = [0] * (holding_period - 1)
    
    # Initial investment (negative cash flow)
    cash_flows = [-equity_invested]
    
    # Add intermediate cash flows
    cash_flows.extend(annual_cash_flows)
    
    # Add exit value
    cash_flows.append(exit_value)
    
    # Calculate IRR
    irr = calculate_irr(cash_flows)
    
    # Calculate MOIC
    total_inflows = sum(cf for cf in cash_flows if cf > 0)
    moic = total_inflows / equity_invested if equity_invested > 0 else 0
    
    return {
        'irr': irr,
        'moic': moic,
        'cash_flows': cash_flows
    }

def run(data, debt_pct, interest_rate, exit_multiple, exit_year, holding_period):
    """Run LBO analysis and return outputs."""
    if not data or not data.get('financials') or data['financials']['income'].empty:
        return None
    
    # Get initial financials
    initial_revenue = data['financials']['income'].iloc[0]['revenues']
    initial_ebitda = initial_revenue * 0.15  # Simplified EBITDA assumption
    
    # Calculate purchase and exit values
    purchase_price = initial_ebitda * exit_multiple
    
    # Project exit EBITDA with growth
    exit_ebitda = initial_ebitda * (1.08 ** holding_period)  # Assume 8% annual EBITDA growth
    exit_value = exit_ebitda * exit_multiple
    
    # Calculate equity and debt components
    equity_invested = purchase_price * (1 - debt_pct/100)
    initial_debt = purchase_price * (debt_pct/100)
    
    # Calculate debt schedule
    debt_schedule = calculate_debt_schedule(purchase_price, debt_pct, interest_rate, holding_period)
    
    # Calculate annual free cash flows (simplified)
    annual_cash_flows = []
    for year in range(holding_period - 1):
        ebitda = initial_ebitda * (1.08 ** (year + 1))
        debt_service = debt_schedule.iloc[year]['Total Payment']
        fcf = ebitda * 0.6 - debt_service  # Assume 60% EBITDA conversion to FCF
        annual_cash_flows.append(fcf)
    
    # Calculate returns
    returns = calculate_returns(
        purchase_price=purchase_price,
        exit_value=exit_value,
        equity_invested=equity_invested,
        holding_period=holding_period,
        annual_cash_flows=annual_cash_flows
    )
    
    return {
        'purchase_price': purchase_price,
        'exit_value': exit_value,
        'equity_invested': equity_invested,
        'initial_debt': initial_debt,
        'debt_schedule': debt_schedule,
        'irr': returns['irr'],
        'moic': returns['moic'],
        'cash_flows': returns['cash_flows'],
        'leverage_ratio': initial_debt / initial_ebitda
    }

def display(outputs):
    """Display LBO analysis results."""
    if not outputs:
        st.warning("No LBO analysis results to display.")
        return
    
    # Display key metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Purchase Price", format_currency(outputs['purchase_price']))
    with col2:
        st.metric("Exit Value", format_currency(outputs['exit_value']))
    with col3:
        st.metric("Initial Leverage", f"{outputs['leverage_ratio']:.1f}x")
    
    # Display returns
    st.subheader("Returns Analysis")
    col1, col2 = st.columns(2)
    with col1:
        irr_value = outputs['irr']
        if irr_value is not None:
            st.metric("IRR", format_percentage(irr_value))
        else:
            st.metric("IRR", "N/A")
    with col2:
        st.metric("MOIC", f"{outputs['moic']:.2f}x")
    
    # Display cash flows
    st.subheader("Cash Flow Summary")
    cash_flows = outputs['cash_flows']
    years = list(range(len(cash_flows)))
    cf_df = pd.DataFrame({
        'Year': years,
        'Cash Flow': cash_flows
    })
    st.dataframe(cf_df.style.format({
        'Cash Flow': '${:,.0f}'
    }))

def display_debt_schedule(outputs):
    """Display debt repayment schedule."""
    if not outputs or 'debt_schedule' not in outputs:
        st.warning("No debt schedule available.")
        return
    
    st.subheader("Debt Repayment Schedule")
    
    # Create waterfall chart
    fig = go.Figure()
    
    schedule = outputs['debt_schedule']
    fig.add_trace(go.Waterfall(
        name="Debt Balance",
        orientation="v",
        measure=["relative"] * len(schedule),
        x=schedule['Year'],
        y=-schedule['Principal Payment'],
        connector={"line": {"color": neon_palette()[0]}},
        decreasing={"marker": {"color": neon_palette()[1]}},
        increasing={"marker": {"color": neon_palette()[0]}}
    ))
    
    fig.update_layout(
        title="Debt Amortization Schedule",
        showlegend=True,
        template="plotly_dark",
        plot_bgcolor="#18181b",
        paper_bgcolor="#18181b",
        font=dict(color="#00ffe7")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display detailed schedule
    st.dataframe(
        schedule.style.format({
            'Beginning Balance': '${:,.0f}',
            'Principal Payment': '${:,.0f}',
            'Interest Payment': '${:,.0f}',
            'Total Payment': '${:,.0f}',
            'Ending Balance': '${:,.0f}'
        })
    ) 