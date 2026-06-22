import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Mr. Tea Franchise Simulator", layout="wide", initial_sidebar_state="expanded")

# --- CUSTOM CSS FOR AESTHETICS ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        text-align: center;
        border: 1px solid #333;
    }
    .metric-value { font-size: 2rem; font-weight: bold; color: #4CAF50; }
    .metric-label { font-size: 1rem; color: #AAAAAA; }
    </style>
""", unsafe_allow_html=True)

st.title("🧋 Mr. Tea Franchise Financial Simulator")
st.markdown("Interactive forecasting dashboard for Khan Market operations.")
st.divider()

# --- SIDEBAR INPUTS (THE SLIDERS) ---
with st.sidebar:
    st.header("⚙️ Operational Variables")
    
    st.subheader("Revenue Drivers")
    orders_per_day = st.slider("Daily Orders", min_value=30, max_value=250, value=125, step=5)
    selling_price = st.slider("Selling Price (₹)", min_value=250, max_value=600, value=400, step=10)
    
    st.subheader("Unit Economics (Per Drink)")
    cogs = st.slider("Raw Material Cost (₹)", min_value=40, max_value=150, value=100, step=5)
    packaging = st.slider("Packaging Cost (₹)", min_value=10, max_value=40, value=25, step=1)
    wastage_pct = st.slider("Wastage Buffer (%)", min_value=0.0, max_value=10.0, value=5.0, step=0.5)
    
    st.subheader("Fixed Costs (Monthly)")
    rent = st.slider("Monthly Rent (₹)", min_value=100000, max_value=400000, value=250000, step=10000)
    staff = st.slider("Staff Cost (₹)", min_value=30000, max_value=150000, value=60000, step=5000)
    utilities = st.slider("Utilities & Misc (₹)", min_value=10000, max_value=50000, value=20000, step=2000)
    
    st.subheader("Franchise & Partnership")
    royalty_pct = st.slider("Franchise Royalty (%)", min_value=0.0, max_value=15.0, value=5.0, step=0.5)
    partner_retainer = st.number_input("Your Base Retainer (₹)", value=30000, step=5000)
    partner_equity = st.slider("Your Profit Share (%)", min_value=5.0, max_value=30.0, value=15.0, step=1.0)

# --- CALCULATIONS ---
days_in_month = 30
monthly_orders = orders_per_day * days_in_month

# Revenue
monthly_revenue = monthly_orders * selling_price

# Variable Costs
wastage_cost = cogs * (wastage_pct / 100)
royalty_cost_per_drink = selling_price * (royalty_pct / 100)
total_variable_cost_per_drink = cogs + packaging + wastage_cost + royalty_cost_per_drink
total_monthly_variable_costs = total_variable_cost_per_drink * monthly_orders

# Fixed Costs
total_monthly_fixed_costs = rent + staff + utilities

# Profit
monthly_net_profit = monthly_revenue - total_monthly_variable_costs - total_monthly_fixed_costs
annual_revenue = monthly_revenue * 12
margin_pct = (monthly_net_profit / monthly_revenue) * 100 if monthly_revenue > 0 else 0

# Breakeven Calculation
contribution_margin_per_drink = selling_price - total_variable_cost_per_drink
if contribution_margin_per_drink > 0:
    breakeven_drinks_monthly = total_monthly_fixed_costs / contribution_margin_per_drink
    breakeven_drinks_daily = int(breakeven_drinks_monthly / days_in_month)
else:
    breakeven_drinks_daily = "N/A"

# Partner Payout Calculation
if monthly_net_profit > 0:
    partner_payout = partner_retainer + (monthly_net_profit * (partner_equity / 100))
else:
    partner_payout = partner_retainer

# --- KPI CARDS ROW ---
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Monthly Net Profit</div>
            <div class="metric-value">₹{monthly_net_profit:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Net Margin</div>
            <div class="metric-value" style="color: {'#4CAF50' if margin_pct > 0 else '#FF5252'};">{margin_pct:.1f}%</div>
        </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Daily Breakeven</div>
            <div class="metric-value" style="color: #FFC107;">{breakeven_drinks_daily} orders</div>
        </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Your Payout</div>
            <div class="metric-value" style="color: #03A9F4;">₹{partner_payout:,.0f}</div>
        </div>
    """, unsafe_allow_html=True)

st.write("") # Spacer
st.write("") # Spacer

# --- CHARTS ROW ---
chart_col1, chart_col2 = st.columns([2, 1])

# Chart 1: Breakeven Curve (Plotly)
with chart_col1:
    st.subheader("📈 Breakeven Analysis & Growth Curve")
    
    # Generate data for the curve
    sim_orders = np.arange(0, 301, 10)
    sim_revenue = sim_orders * days_in_month * selling_price
    sim_var_costs = sim_orders * days_in_month * total_variable_cost_per_drink
    sim_total_costs = sim_var_costs + total_monthly_fixed_costs
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sim_orders, y=sim_revenue, mode='lines', name='Revenue', line=dict(color='#4CAF50', width=3)))
    fig.add_trace(go.Scatter(x=sim_orders, y=sim_total_costs, mode='lines', name='Total Costs', line=dict(color='#FF5252', width=3)))
    
    # Highlight current position
    fig.add_trace(go.Scatter(x=[orders_per_day], y=[monthly_revenue], mode='markers', name='Current Target', 
                             marker=dict(color='#03A9F4', size=12, symbol='star')))
    
    fig.update_layout(
        xaxis_title="Daily Orders",
        yaxis_title="Monthly Value (₹)",
        template="plotly_dark",
        hovermode="x unified",
        margin=dict(l=0, r=0, t=30, b=0),
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
    )
    st.plotly_chart(fig, use_container_width=True)

# Chart 2: Expense Breakdown (Plotly Donut)
with chart_col2:
    st.subheader("🍩 Monthly Expense Breakdown")
    
    expenses = {
        'Rent': rent,
        'Staff': staff,
        'Utilities': utilities,
        'Raw Materials': cogs * monthly_orders,
        'Packaging': packaging * monthly_orders,
        'Wastage': wastage_cost * monthly_orders,
        'Franchise Royalty': royalty_cost_per_drink * monthly_orders
    }
    
    df_exp = pd.DataFrame(list(expenses.items()), columns=['Category', 'Amount'])
    # Filter out 0 amounts
    df_exp = df_exp[df_exp['Amount'] > 0]
    
    fig2 = px.pie(df_exp, values='Amount', names='Category', hole=0.6, template="plotly_dark",
                  color_discrete_sequence=px.colors.sequential.Tealgrn)
    
    fig2.update_traces(textposition='inside', textinfo='percent+label', showlegend=False)
    fig2.update_layout(margin=dict(l=0, r=0, t=30, b=0))
    
    st.plotly_chart(fig2, use_container_width=True)