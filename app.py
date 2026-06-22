
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Mr Tea Financial Intelligence Center",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# PREMIUM LIGHT THEME
# =====================================================

st.markdown("""
<style>

.stApp{
    background:#F8FAFC;
}

section[data-testid="stSidebar"]{
    background:#FFFFFF;
    border-right:1px solid #E2E8F0;
}

.block-container{
    max-width:1450px;
    padding-top:1.5rem;
}

div[data-testid="stVerticalBlock"]{
    gap:1rem;
}

.card{
    background:white;
    padding:22px;
    border-radius:18px;
    border:1px solid #E2E8F0;
    box-shadow:0px 4px 20px rgba(0,0,0,0.04);
}

.kpi-title{
    color:#64748B;
    font-size:12px;
    text-transform:uppercase;
    letter-spacing:1px;
    font-weight:600;
}

.kpi-value{
    font-size:34px;
    font-weight:700;
    color:#0F172A;
}

.main-title{
    font-size:38px;
    font-weight:700;
    color:#0F172A;
}

.subtitle{
    color:#64748B;
    font-size:16px;
}

.section-title{
    font-size:22px;
    font-weight:700;
    color:#0F172A;
    margin-bottom:12px;
}

hr{
    border-color:#E2E8F0 !important;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.title("Financial Drivers")

    st.markdown("---")

    st.subheader("Revenue Drivers")

    orders_per_day = st.slider(
        "Daily Orders",
        30,
        300,
        125,
        5
    )

    selling_price = st.slider(
        "Average Ticket Size (₹)",
        250,
        600,
        400,
        10
    )

    st.markdown("---")

    st.subheader("Variable Costs")

    cogs = st.slider(
        "Raw Material (₹)",
        40,
        150,
        100,
        5
    )

    packaging = st.slider(
        "Packaging (₹)",
        10,
        40,
        25
    )

    wastage_pct = st.slider(
        "Wastage %",
        0.0,
        10.0,
        5.0,
        0.5
    )

    royalty_pct = st.slider(
        "Royalty %",
        0.0,
        15.0,
        5.0,
        0.5
    )

    st.markdown("---")

    st.subheader("Fixed Costs")

    rent = st.slider(
        "Rent",
        100000,
        400000,
        250000,
        10000
    )

    staff = st.slider(
        "Staff",
        30000,
        150000,
        60000,
        5000
    )

    utilities = st.slider(
        "Utilities",
        10000,
        50000,
        20000,
        2000
    )

# =====================================================
# CALCULATIONS
# =====================================================

days = 30

monthly_volume = orders_per_day * days

monthly_revenue = monthly_volume * selling_price

annual_revenue = monthly_revenue * 12

wastage_cost = cogs * (wastage_pct / 100)

royalty_cost = selling_price * (royalty_pct / 100)

unit_variable_cost = (
    cogs
    + packaging
    + wastage_cost
    + royalty_cost
)

monthly_variable_cost = (
    unit_variable_cost
    * monthly_volume
)

fixed_cost = (
    rent
    + staff
    + utilities
)

monthly_profit = (
    monthly_revenue
    - monthly_variable_cost
    - fixed_cost
)

annual_profit = monthly_profit * 12

profit_margin = (
    monthly_profit / monthly_revenue * 100
)

contribution_margin = (
    selling_price
    - unit_variable_cost
)

if contribution_margin > 0:
    breakeven_units_month = (
        fixed_cost
        / contribution_margin
    )
    breakeven_daily = int(
        breakeven_units_month / days
    )
else:
    breakeven_daily = 0

# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="main-title">
Mr Tea Financial Intelligence Center
</div>

<div class="subtitle">
Strategic Franchise Performance Dashboard • Khan Market
</div>
""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# KPI CARDS
# =====================================================

def metric_card(title, value, color):

    st.markdown(
        f"""
        <div class="card">
            <div class="kpi-title">
            {title}
            </div>

            <div class="kpi-value"
            style="color:{color}">
            {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

c1,c2,c3,c4 = st.columns(4)

with c1:
    metric_card(
        "Monthly Revenue",
        f"₹{monthly_revenue:,.0f}",
        "#2563EB"
    )

with c2:
    metric_card(
        "Monthly Profit",
        f"₹{monthly_profit:,.0f}",
        "#10B981"
    )

with c3:
    metric_card(
        "Profit Margin",
        f"{profit_margin:.1f}%",
        "#F59E0B"
    )

with c4:
    metric_card(
        "Break-even Volume",
        f"{breakeven_daily}",
        "#EF4444"
    )

st.markdown("<br>", unsafe_allow_html=True)

# =====================================================
# REVENUE COST PROFIT TREND
# =====================================================

left,right = st.columns([3,1])

with left:

    volume_range = np.arange(
        30,
        301,
        10
    )

    revenues = (
        volume_range
        * days
        * selling_price
    )

    costs = (
        volume_range
        * days
        * unit_variable_cost
        + fixed_cost
    )

    profits = (
        revenues
        - costs
    )

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=volume_range,
            y=revenues,
            name="Revenue",
            line=dict(
                width=4,
                color="#2563EB"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=volume_range,
            y=costs,
            name="Costs",
            line=dict(
                width=4,
                color="#EF4444"
            )
        )
    )

    fig.add_trace(
        go.Scatter(
            x=volume_range,
            y=profits,
            name="Profit",
            line=dict(
                width=4,
                color="#10B981"
            )
        )
    )

    fig.update_layout(
        title="Revenue vs Cost vs Profit",
        template="plotly_white",
        height=450
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

# =====================================================
# GAUGE
# =====================================================

with right:

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=profit_margin,
            title={
                "text":"Profit Margin"
            },
            gauge={
                "axis":{
                    "range":[0,50]
                },
                "bar":{
                    "color":"#10B981"
                },
                "steps":[
                    {
                        "range":[0,15],
                        "color":"#FEE2E2"
                    },
                    {
                        "range":[15,30],
                        "color":"#FEF3C7"
                    },
                    {
                        "range":[30,50],
                        "color":"#DCFCE7"
                    }
                ]
            }
        )
    )

    gauge.update_layout(
        height=450
    )

    st.plotly_chart(
        gauge,
        use_container_width=True
    )

# =====================================================
# DONUT + WATERFALL
# =====================================================

left,right = st.columns(2)

with left:

    cost_data = pd.DataFrame({
        "Category":[
            "Rent",
            "Staff",
            "Utilities",
            "Raw Material",
            "Packaging",
            "Wastage",
            "Royalty"
        ],
        "Value":[
            rent,
            staff,
            utilities,
            cogs*monthly_volume,
            packaging*monthly_volume,
            wastage_cost*monthly_volume,
            royalty_cost*monthly_volume
        ]
    })

    donut = px.pie(
        cost_data,
        names="Category",
        values="Value",
        hole=0.72,
        color_discrete_sequence=[
            "#2563EB",
            "#10B981",
            "#F59E0B",
            "#EF4444",
            "#8B5CF6",
            "#14B8A6",
            "#EC4899"
        ]
    )

    donut.update_layout(
        title="Cost Allocation Structure",
        height=500
    )

    st.plotly_chart(
        donut,
        use_container_width=True
    )

with right:

    waterfall = go.Figure(
        go.Waterfall(
            name="PnL",
            orientation="v",
            measure=[
                "relative",
                "relative",
                "relative",
                "relative",
                "relative",
                "relative",
                "relative",
                "total"
            ],
            x=[
                "Revenue",
                "COGS",
                "Packaging",
                "Wastage",
                "Royalty",
                "Rent",
                "Staff+Utilities",
                "Profit"
            ],
            y=[
                monthly_revenue,
                -cogs*monthly_volume,
                -packaging*monthly_volume,
                -wastage_cost*monthly_volume,
                -royalty_cost*monthly_volume,
                -rent,
                -(staff+utilities),
                0
            ]
        )
    )

    waterfall.update_layout(
        title="Monthly P&L Waterfall",
        template="plotly_white",
        height=500
    )

    st.plotly_chart(
        waterfall,
        use_container_width=True
    )

# =====================================================
# UNIT ECONOMICS
# =====================================================

unit_df = pd.DataFrame({
    "Metric":[
        "Raw Material",
        "Packaging",
        "Wastage",
        "Royalty",
        "Contribution Margin"
    ],
    "Value":[
        cogs,
        packaging,
        wastage_cost,
        royalty_cost,
        contribution_margin
    ]
})

bar = px.bar(
    unit_df,
    x="Metric",
    y="Value",
    color="Metric",
    text="Value"
)

bar.update_layout(
    title="Unit Economics",
    template="plotly_white",
    height=500,
    showlegend=False
)

st.plotly_chart(
    bar,
    use_container_width=True
)

# =====================================================
# BREAK EVEN
# =====================================================

volumes = np.arange(
    0,
    350,
    5
)

revenue_curve = (
    volumes
    * days
    * selling_price
)

cost_curve = (
    volumes
    * days
    * unit_variable_cost
    + fixed_cost
)

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=volumes,
        y=revenue_curve,
        name="Revenue"
    )
)

fig.add_trace(
    go.Scatter(
        x=volumes,
        y=cost_curve,
        name="Total Cost"
    )
)

fig.add_vline(
    x=breakeven_daily,
    line_dash="dash",
    line_color="red"
)

fig.update_layout(
    title="Break-Even Analysis",
    template="plotly_white",
    height=500
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# =====================================================
# SCENARIO ANALYSIS
# =====================================================

st.subheader(
    "Scenario Analysis Matrix"
)

scenario_orders = [
    75,
    100,
    125,
    150,
    175,
    200
]

rows = []

for orders in scenario_orders:

    vol = orders * days

    rev = (
        vol
        * selling_price
    )

    var_cost = (
        vol
        * unit_variable_cost
    )

    prof = (
        rev
        - var_cost
        - fixed_cost
    )

    rows.append([
        orders,
        round(rev),
        round(prof)
    ])

scenario_df = pd.DataFrame(
    rows,
    columns=[
        "Daily Orders",
        "Revenue",
        "Profit"
    ]
)

st.dataframe(
    scenario_df,
    use_container_width=True,
    hide_index=True
)

# =====================================================
# FOOTER
# =====================================================

st.markdown("<br><br>", unsafe_allow_html=True)

st.caption(
    "Financial Intelligence Dashboard • Strategic Simulation Environment"
)

