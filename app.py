import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

# --- INITIAL APP SPECIFICATIONS ---
st.set_page_config(
    page_title="Mr. Tea — Corporate Performance Dashboard",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- PREMIUM CORPORATE DARK THEME STYLING ---
st.markdown("""
    <style>
    /* Main Background adjustments */
    .stApp {
        background-color: #0F0F12;
    }
    /* Container/Card design */
    div[data-testid="stMetric"] {
        background-color: #16161D;
        border: 1px solid #23232F;
        padding: 24px 20px;
        border-radius: 12px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
    }
    div[data-testid="stMetric"] label {
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem !important;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #8E8E9F !important;
    }
    div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
        font-family: 'Inter', sans-serif;
        font-size: 2.2rem !important;
        font-weight: 700 !important;
        color: #FFFFFF !important;
    }
    /* Section Headers */
    .section-header {
        font-family: 'Inter', sans-serif;
        font-size: 1.25rem;
        font-weight: 600;
        color: #E4E4E7;
        margin-bottom: 16px;
        letter-spacing: 0.5px;
    }
    hr {
        border-color: #23232F !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- HEADER SECTION ---
st.title("🧋 Mr. Tea — Strategic Financial Architecture")
st.markdown("<p style='color: #8E8E9F; font-size: 1.1rem;'>Enterprise Projections & Operational Risk Analysis for Khan Market</p>", unsafe_allow_html=True)
st.divider()

# --- SIDEBAR INPUT ENGINE (CLEAN & CORPORATE) ---
with st.sidebar:
    st.header("📋 Core Model Inputs")
    st.markdown("---")
    
    st.subheader("📈 Scale & Pricing")
    orders_per_day = st.slider("Target Daily Orders", min_value=30, max_value=300, value=125, step=5)
    selling_price = st.slider("Average Ticket Size (₹)", min_value=250, max_value=600, value=400, step=10)
    
    st.subheader("📦 Variable Costs (Per Unit)")
    cogs = st.slider("Raw Material Supply (₹)", min_value=40, max_value=150, value=100, step=5)
    packaging = st.slider("Premium Packaging (₹)", min_value=10, max_value=40, value=25, step=1)
    wastage_pct = st.slider("Wastage Buffer Allowance (%)", min_value=0.0, max_value=10.0, value=5.0, step=0.5)
    
    st.subheader("🏢 Structural Fixed Overhead")
    rent = st.slider("Monthly Lease Capital (₹)", min_value=100000, max_value=400000, value=250000, step=10000)
    staff = st.slider("Operational Workforce (₹)", min_value=30000, max_value=150000, value=60000, step=5000)
    utilities = st.slider("Utilities & Infrastructure (₹)", min_value=10000, max_value=50000, value=20000, step=2000)
    
    st.subheader("🎗️ Franchise Commitments")
    royalty_pct = st.slider("Gross Royalty Obligation (%)", min_value=0.0, max_value=15.0, value=5.0, step=0.5)

# --- FINANCIAL ENGINE CALCULATIONS ---
days_in_month = 30
monthly_volume = orders_per_day * days_in_month

# Top-Line Revenue
monthly_gross_revenue = monthly_volume * selling_price
annual_gross_revenue = monthly_gross_revenue * 12

# Unit Cost Math
wastage_impact = cogs * (wastage_pct / 100)
royalty_impact = selling_price * (royalty_pct / 100)
unit_variable_cost = cogs + packaging + wastage_impact + royalty_impact
total_monthly_variable_costs = unit_variable_cost * monthly_volume

# Fixed Cost Math
total_monthly_fixed_costs = rent + staff + utilities

# Net Profit Realization
monthly_net_profit = monthly_gross_revenue - total_monthly_variable_costs - total_monthly_fixed_costs
annual_net_profit = monthly_net_profit * 12
net_profit_margin = (monthly_net_profit / monthly_gross_revenue) * 100 if monthly_gross_revenue > 0 else 0

# Dynamic Break-Even Analysis
contribution_margin_per_unit = selling_price - unit_variable_cost
if contribution_margin_per_unit > 0:
    required_monthly_breakeven = total_monthly_fixed_costs / contribution_margin_per_unit
    required_daily_breakeven = int(required_monthly_breakeven / days_in_month)
else:
    required_daily_breakeven = 0

# --- METRIC SUMMARY MATRIX ---
m_col1, m_col2, m_col3, m_col4 = st.columns(4)

with m_col1:
    st.metric(label="Monthly Net Profit", value=f"₹{monthly_net_profit:,.0f}")
with m_col2:
    st.metric(label="Net Profit Margin", value=f"{net_profit_margin:.1f}%")
with m_col3:
    st.metric(label="Daily Break-Even Vol", value=f"{required_daily_breakeven} units")
with m_col4:
    st.metric(label="Annualized Net Run-Rate", value=f"₹{annual_net_profit:,.0f}")

st.write("")
st.write("")

# --- VISUALIZATION LAYER ---
# Row 1: Primary Growth & Structural Breakdowns
c_col1, c_col2 = st.columns([2, 1])

with c_col1:
    st.markdown('<div class="section-header">📈 Break-Even Threshold & Scale Geometry</div>', unsafe_allow_html=True)
    
    # Generate data vector for visualization
    volume_axis = np.arange(0, 351, 10)
    rev_curve = volume_axis * days_in_month * selling_price
    var_cost_curve = volume_axis * days_in_month * unit_variable_cost
    total_cost_curve = var_cost_curve + total_monthly_fixed_costs
    
    fig_growth = go.Figure()
    
    # Revenue Curve Line
    fig_growth.add_trace(go.Scatter(
        x=volume_axis, y=rev_curve, mode='lines', name='Gross Revenue Target',
        line=dict(color='#10B981', width=3, dash='solid')
    ))
    
    # Total Operational Outlays Line
    fig_growth.add_trace(go.Scatter(
        x=volume_axis, y=total_cost_curve, mode='lines', name='Total Operational Outlay',
        line=dict(color='#EF4444', width=3, dash='solid')
    ))
    
    # Current Target Intersection Pointer
    fig_growth.add_trace(go.Scatter(
        x=[orders_per_day], y=[monthly_gross_revenue], mode='markers+text', name='Current Target Allocation',
        marker=dict(color='#3B82F6', size=12, symbol='circle', line=dict(color='#FFFFFF', width=2)),
        text=[f"  ₹{monthly_gross_revenue:,.0f}"], textposition="middle right", textfont=dict(color='#FFFFFF')
    ))
    
    fig_growth.update_layout(
        xaxis=dict(title="Daily Order Volume", gridcolor='#1E1E2F', zeroline=False),
        yaxis=dict(title="Monthly Value Matrix (₹)", gridcolor='#1E1E2F', zeroline=False),
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        hovermode="x unified",
        margin=dict(l=10, r=10, t=10, b=10),
        legend=dict(yanchor="top", y=0.95, xanchor="left", x=0.05, bgcolor='rgba(22,22,29,0.8)')
    )
    st.plotly_chart(fig_growth, use_container_width=True)

with c_col2:
    st.markdown('<div class="section-header">🍩 Asset & Cost Allocation</div>', unsafe_allow_html=True)
    
    allocation_matrix = {
        'Lease Capital (Rent)': rent,
        'Workforce (Staff)': staff,
        'Infrastructure (Utilities)': utilities,
        'Raw Material Pipeline': cogs * monthly_volume,
        'Custom Packaging': packaging * monthly_volume,
        'Wastage Overhead': wastage_impact * monthly_volume,
        'Franchise Royalty Fee': royalty_impact * monthly_volume
    }
    
    df_alloc = pd.DataFrame(list(allocation_matrix.items()), columns=['Cost Center', 'Capital Outlay'])
    df_alloc = df_alloc[df_alloc['Capital Outlay'] > 0]
    
    fig_donut = px.pie(
        df_alloc, values='Capital Outlay', names='Cost Center', hole=0.65,
        template="plotly_dark",
        color_discrete_sequence=px.colors.sequential.Slate_r
    )
    
    fig_donut.update_traces(textposition='outside', textinfo='percent', showlegend=True)
    fig_donut.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=10, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_donut, use_container_width=True)

st.divider()

# Row 2: Deep Unit Economics Matrix
st.markdown('<div class="section-header">📊 Unit Economics Comparison (Per Single Unit vs Revenue)</div>', unsafe_allow_html=True)

unit_metrics = {
    'Cost Element': ['Raw Supply', 'Packaging', 'Wastage Buffer', 'Royalty Fee', 'Net Contribution Margin'],
    'Value (₹)': [cogs, packaging, wastage_impact, royalty_impact, contribution_margin_per_unit]
}
df_unit = pd.DataFrame(unit_metrics)

fig_bar = px.bar(
    df_unit, x='Cost Element', y='Value (₹)',
    template="plotly_dark",
    text='Value (₹)',
    color='Cost Element',
    color_discrete_sequence=px.colors.qualitative.Muted
)

fig_bar.update_traces(texttemplate='₹%{text:.2f}', textposition='outside')
fig_bar.update_layout(
    xaxis=dict(title="", showgrid=False),
    yaxis=dict(title="Rupees (₹)", gridcolor='#1E1E2F', range=[0, max(selling_price, contribution_margin_per_unit) * 1.15]),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    showlegend=False,
    margin=dict(l=10, r=10, t=20, b=10)
)
st.plotly_chart(fig_bar, use_container_width=True)
