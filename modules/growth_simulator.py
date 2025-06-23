import streamlit as st
import numpy as np
import plotly.graph_objs as go
from modules.utils import neon_palette

def simulate_growth_scenarios(base_value, years, scenarios):
    """Simulate different growth scenarios."""
    results = {}
    for name, growth_rate in scenarios.items():
        values = [base_value]
        for _ in range(years):
            values.append(values[-1] * (1 + growth_rate/100))
        results[name] = values
    return results

def display():
    """Display growth simulation interface and results."""
    st.subheader("Growth Trajectory Simulator")
    
    col1, col2 = st.columns(2)
    with col1:
        base_value = st.number_input("Initial Value ($M)", value=100.0, step=10.0)
        years = st.slider("Projection Years", 1, 10, 5)
    
    with col2:
        bear_growth = st.slider("Bear Case Growth (%)", -20, 20, 0)
        base_growth = st.slider("Base Case Growth (%)", -10, 30, 8)
        bull_growth = st.slider("Bull Case Growth (%)", 0, 50, 15)
    
    scenarios = {
        "Bear Case": bear_growth,
        "Base Case": base_growth,
        "Bull Case": bull_growth
    }
    
    results = simulate_growth_scenarios(base_value, years, scenarios)
    
    # Create plot
    fig = go.Figure()
    colors = neon_palette()
    
    for i, (scenario, values) in enumerate(results.items()):
        fig.add_trace(go.Scatter(
            x=list(range(years + 1)),
            y=values,
            name=scenario,
            line=dict(color=colors[i], width=3),
            mode='lines+markers'
        ))
    
    fig.update_layout(
        title="Growth Scenarios",
        xaxis_title="Year",
        yaxis_title="Value ($M)",
        template="plotly_dark",
        plot_bgcolor="#18181b",
        paper_bgcolor="#18181b",
        font=dict(color="#00ffe7")
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display table of values
    st.subheader("Projected Values")
    for scenario, values in results.items():
        st.write(f"{scenario}: ${values[-1]:.1f}M (Year {years})") 