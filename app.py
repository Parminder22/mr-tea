import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ==========================================
# 1. PAGE CONFIGURATION & GLOBAL SETUP
# ==========================================
st.set_page_config(
    page_title="Executive Financial Model | Mr. Tea",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Corporate Light Theme CSS (Stripe/Linear/Vercel aesthetic)
st.markdown("""
    <style>
    /* Global Reset & Backgrounds */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    .stApp {
        background-color: #F8FAFC;
    }
    
    /* Hide Streamlit Defaults */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 1400px;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #F1F5F9;
        border-right: 1px solid #E2E8F0;
    }
    
    /* Custom Header Typography */
    .dash-title {
        font-size: 36px;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 4px;
        letter-spacing: -0.5px;
    }
    .dash-subtitle {
        font-size: 16px;
        color: #64748B;
        font-weight: 400;
        margin-bottom: 32px;
    }
    .section-header {
        font-size: 20px;
        font-weight: 600;
        color: #0F172A;
        margin-top: 24px;
        margin-bottom: 16px;
        padding-bottom: 8px;
        border-bottom: 1px solid #E2E8F0;
    }
    
    /* Premium KPI Cards */
    .kpi-container {
        display: flex;
        justify-content: space-between;
        gap: 16px;
        margin-bottom: 32px;
    }
    .kpi-card {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 12px;
        padding: 24px;
        flex: 1;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.025);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
        border-top: 4px solid #2563EB;
    }
    .kpi-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 15px -3px rgba(0,0,0,0.05), 0 4px 6px -2px rgba(0,0,0,0.025);
    }
    .kpi-card.green { border-top-color: #10B981; }
    .kpi-card.orange { border-top-color: #F59E0B; }
    .kpi-card.purple { border-top-color: #8B5CF6; }
    
    .kpi-label {
        font-size: 13px;
        text-transform: uppercase;
        font-weight: 600;
        color: #64748B;
        letter-spacing: 0.5px;
        margin-bottom: 8px;
    }
    .kpi-value {
        font-size: 32px;
        font-weight: 700;
        color: #0F172A;
    }
    </style>
""", unsafe_allow_html=True)

# Plotly Configuration to remove floating menus
PLOTLY_CONFIG = {'displayModeBar': False}

# ==========================================
# 2. DATA ENGINE & CALCULATIONS
# ==========================================
class FinancialEngine:
    def __init__(self, orders, price, cogs, packaging, wastage_pct, royalty_pct, rent, staff, utilities):
        self.days = 30
        self.orders_per_day = orders
        self.monthly_volume = orders * self.days
        self.selling_price = price
        
        # Variable Costs
        self.cogs = cogs
        self.packaging = packaging
        self.wastage = cogs * (wastage_pct / 100)
        self.royalty = price * (royalty_pct / 100)
        self.unit_vc = self.cogs + self.packaging + self.wastage + self.royalty
        self.total_vc = self.unit_vc * self.monthly_volume
        
        # Fixed Costs
        self.rent = rent
        self.staff = staff
        self.utilities = utilities
        self.total_fc = rent + staff + utilities
        
        # Margins & Profit
        self.cm_per_unit = price - self.unit_vc
        self.revenue = self.monthly_volume * price
        self.net_profit = self.revenue - self.total_vc - self.total_fc
        self.margin_pct = (self.net_profit / self.revenue * 100) if self.revenue > 0 else 0
        
        # Operational Metrics
        self.breakeven_vol = int(self.total_fc / self.cm_per_unit) if self.cm_per_unit > 0 else 0
        self.breakeven_daily = int(self.breakeven_vol / self.days)

    def get_health_score(self):
        score = 100
        if self.margin_pct < 15: score -= 20
        elif self.margin_pct < 25: score -= 10
        if self.breakeven_daily > (self.orders_per_day * 0.8): score -= 25
        if self.cm_per_unit < (self.selling_price * 0.4): score -= 15
        return max(0, min(100, int(score)))

# ==========================================
# 3. SIDEBAR (INPUT CONTROLS)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #0F172A; font-size: 20px; margin-bottom: 24px;'>Control Panel</h2>", unsafe_allow_html=True)
    
    orders = st.slider("Daily Orders", 30, 300, 125, 5)
    price = st.slider("Average Ticket Size (₹)", 250, 600, 400, 10)
    
    st.markdown("---")
    st.markdown("<p style='font-size: 14px; font-weight: 600; color: #64748B;'>UNIT ECONOMICS</p>", unsafe_allow_html=True)
    cogs = st.slider("Raw Material (₹)", 40, 150, 100, 5)
    pkg = st.slider("Packaging (₹)", 10, 40, 25, 1)
    wastage = st.slider("Wastage Buffer (%)", 0.0, 10.0, 5.0, 0.5)
    royalty = st.slider("Franchise Royalty (%)", 0.0, 15.0, 5.0, 0.5)
    
    st.markdown("---")
    st.markdown("<p style='font-size: 14px; font-weight: 600; color: #64748B;'>FIXED OVERHEAD (MONTHLY)</p>", unsafe_allow_html=True)
    rent = st.slider("Lease / Rent (₹)", 100000, 400000, 250000, 10000)
    staff = st.slider("Staff Payroll (₹)", 30000, 150000, 60000, 5000)
    utils = st.slider("Utilities & Misc (₹)", 10000, 50000, 20000, 2000)

engine = FinancialEngine(orders, price, cogs, pkg, wastage, royalty, rent, staff, utils)

# ==========================================
# 4. TOP HEADER & KPIs
# ==========================================
current_date = datetime.now().strftime("%B %d, %Y")

st.markdown(f"""
    <div>
        <div class='dash-title'>Khan Market Financial Intelligence</div>
        <div class='dash-subtitle'>Strategic projection model & scenario analysis  •  Generated: {current_date}</div>
    </div>
""", unsafe_allow_html=True)

# Custom HTML KPI Cards
st.markdown(f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Monthly Gross Revenue</div>
            <div class="kpi-value">₹{engine.revenue:,.0f}</div>
        </div>
        <div class="kpi-card green">
            <div class="kpi-label">Net Operating Profit</div>
            <div class="kpi-value">₹{engine.net_profit:,.0f}</div>
        </div>
        <div class="kpi-card purple">
            <div class="kpi-label">Net Profit Margin</div>
            <div class="kpi-value">{engine.margin_pct:.1f}%</div>
        </div>
        <div class="kpi-card orange">
            <div class="kpi-label">Daily Break-even Target</div>
            <div class="kpi-value">{engine.breakeven_daily} orders</div>
        </div>
    </div>
""", unsafe_allow_html=True)

# ==========================================
# 5. ROW 1: HERO CHART & HEALTH SCORE
# ==========================================
st.markdown("<div class='section-header'>Enterprise Trajectory & Health</div>", unsafe_allow_html=True)
col1, col2 = st.columns([3, 1])

with col1:
    # 12-Month Projection simulating 3% MoM growth
    months = [f"M{i+1}" for i in range(12)]
    growth_rates = [1.0] + [1.03**i for i in range(1, 12)]
    
    proj_rev = [engine.revenue * g for g in growth_rates]
    proj_vc = [engine.total_vc * g for g in growth_rates]
    proj_profit = [r - v - engine.total_fc for r, v in zip(proj_rev, proj_vc)]
    
    fig_proj = go.Figure()
    fig_proj.add_trace(go.Scatter(x=months, y=proj_rev, name="Projected Revenue", line=dict(color='#2563EB', width=3), fill='tozeroy', fillcolor='rgba(37, 99, 235, 0.05)'))
    fig_proj.add_trace(go.Scatter(x=months, y=proj_profit, name="Projected Profit", line=dict(color='#10B981', width=3)))
    
    fig_proj.update_layout(
        title="12-Month Forward Projection (Assuming 3% MoM Volume Growth)",
        title_font=dict(size=14, color='#64748B'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        hovermode="x unified",
        margin=dict(l=0, r=0, t=40, b=0),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        xaxis=dict(showgrid=False, linecolor='#E2E8F0'),
        yaxis=dict(gridcolor='#F1F5F9', zerolinecolor='#E2E8F0')
    )
    st.plotly_chart(fig_proj, use_container_width=True, config=PLOTLY_CONFIG)

with col2:
    # Executive Health Score Gauge
    score = engine.get_health_score()
    score_color = '#10B981' if score > 75 else '#F59E0B' if score > 50 else '#EF4444'
    
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=score,
        title={'text': "Financial Health Index", 'font': {'size': 14, 'color': '#64748B'}},
        gauge={
            'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#0F172A"},
            'bar': {'color': score_color},
            'bgcolor': "#F1F5F9",
            'borderwidth': 0,
            'steps': [
                {'range': [0, 50], 'color': 'rgba(239, 68, 68, 0.1)'},
                {'range': [50, 75], 'color': 'rgba(245, 158, 11, 0.1)'},
                {'range': [75, 100], 'color': 'rgba(16, 185, 129, 0.1)'}]
        }
    ))
    fig_gauge.update_layout(margin=dict(l=20, r=20, t=40, b=20), paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_gauge, use_container_width=True, config=PLOTLY_CONFIG)

# ==========================================
# 6. ROW 2: P&L WATERFALL & ALLOCATION
# ==========================================
st.markdown("<div class='section-header'>Capital Flow & Cost Architecture</div>", unsafe_allow_html=True)
col3, col4 = st.columns([2, 1])

with col3:
    # Monthly P&L Waterfall
    fig_waterfall = go.Figure(go.Waterfall(
        orientation="v",
        measure=["relative", "relative", "relative", "relative", "relative", "relative", "relative", "total"],
        x=["Gross Revenue", "COGS", "Packaging", "Wastage", "Royalty", "Rent", "Payroll", "Net Profit"],
        textposition="outside",
        texttemplate="₹%{y:,.0s}",
        y=[engine.revenue, -engine.cogs*engine.monthly_volume, -engine.packaging*engine.monthly_volume, 
           -engine.wastage*engine.monthly_volume, -engine.royalty*engine.monthly_volume, 
           -engine.rent, -engine.staff, engine.net_profit],
        connector={"line": {"color": "#E2E8F0"}},
        decreasing={"marker": {"color": "#EF4444"}},
        increasing={"marker": {"color": "#10B981"}},
        totals={"marker": {"color": "#2563EB"}}
    ))
    fig_waterfall.update_layout(
        title="Monthly Profit & Loss Waterfall", title_font=dict(size=14, color='#64748B'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=0),
        yaxis=dict(gridcolor='#F1F5F9', zerolinecolor='#E2E8F0')
    )
    st.plotly_chart(fig_waterfall, use_container_width=True, config=PLOTLY_CONFIG)

with col4:
    # Clean Donut Chart
    labels = ['Rent', 'Payroll', 'Utilities', 'Raw Materials', 'Packaging', 'Royalty']
    values = [engine.rent, engine.staff, engine.utilities, engine.cogs*engine.monthly_volume, 
              engine.packaging*engine.monthly_volume, engine.royalty*engine.monthly_volume]
    
    fig_donut = px.pie(names=labels, values=values, hole=0.7, color_discrete_sequence=['#0F172A', '#334155', '#64748B', '#94A3B8', '#CBD5E1', '#E2E8F0'])
    fig_donut.update_traces(textposition='inside', textinfo='percent')
    fig_donut.update_layout(
        title="Opex Distribution", title_font=dict(size=14, color='#64748B'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=0),
        showlegend=False
    )
    # Add center text
    fig_donut.add_annotation(text="Total Costs", x=0.5, y=0.55, font_size=12, showarrow=False, font_color="#64748B")
    fig_donut.add_annotation(text=f"₹{(engine.total_vc + engine.total_fc):,.0f}", x=0.5, y=0.45, font_size=18, font_weight="bold", showarrow=False)
    
    st.plotly_chart(fig_donut, use_container_width=True, config=PLOTLY_CONFIG)

# ==========================================
# 7. ROW 3: SENSITIVITY & UNIT ECONOMICS
# ==========================================
st.markdown("<div class='section-header'>Risk Analysis & Unit Economics</div>", unsafe_allow_html=True)
col5, col6 = st.columns([1.5, 1])

with col5:
    # Executive Sensitivity Heatmap (Orders vs Price)
    order_range = np.linspace(max(30, engine.orders_per_day * 0.5), engine.orders_per_day * 1.5, 6)
    price_range = np.linspace(250, 600, 6)
    
    z_data = []
    for p in price_range:
        row = []
        for o in order_range:
            temp_eng = FinancialEngine(o, p, engine.cogs, engine.packaging, wastage, royalty, engine.rent, engine.staff, engine.utilities)
            row.append(temp_eng.net_profit)
        z_data.append(row)

    fig_heat = go.Figure(data=go.Heatmap(
        z=z_data, x=[f"{int(o)} orders" for o in order_range], y=[f"₹{int(p)}" for p in price_range],
        colorscale="RdYlGn", text=np.array(z_data), texttemplate="₹%{text:,.0f}", showscale=False
    ))
    fig_heat.update_layout(
        title="Net Profit Sensitivity (Volume vs. Pricing)", title_font=dict(size=14, color='#64748B'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=0),
        xaxis=dict(showgrid=False), yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig_heat, use_container_width=True, config=PLOTLY_CONFIG)

with col6:
    # Unit Economics Stack
    fig_unit = go.Figure()
    fig_unit.add_trace(go.Bar(x=['Cost Stack'], y=[engine.cogs], name='Raw Material', marker_color='#94A3B8'))
    fig_unit.add_trace(go.Bar(x=['Cost Stack'], y=[engine.packaging], name='Packaging', marker_color='#CBD5E1'))
    fig_unit.add_trace(go.Bar(x=['Cost Stack'], y=[engine.wastage], name='Wastage', marker_color='#EF4444'))
    fig_unit.add_trace(go.Bar(x=['Cost Stack'], y=[engine.royalty], name='Royalty', marker_color='#8B5CF6'))
    fig_unit.add_trace(go.Bar(x=['Cost Stack'], y=[engine.cm_per_unit], name='Contribution Margin', marker_color='#10B981'))
    
    fig_unit.update_layout(
        barmode='stack', title="Per-Unit Value Extraction", title_font=dict(size=14, color='#64748B'),
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=40, b=0),
        yaxis=dict(gridcolor='#F1F5F9', zerolinecolor='#E2E8F0', title="Rupees (₹)"),
        showlegend=True, legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
    )
    st.plotly_chart(fig_unit, use_container_width=True, config=PLOTLY_CONFIG)

# ==========================================
# 8. ROW 4: SCENARIO MATRIX TABLE
# ==========================================
st.markdown("<div class='section-header'>Volume Stress Testing</div>", unsafe_allow_html=True)

# Generate Scenario Data
scenarios = []
for vol in [50, 75, 100, 125, 150, 200]:
    se = FinancialEngine(vol, engine.selling_price, engine.cogs, engine.packaging, wastage, royalty, engine.rent, engine.staff, engine.utilities)
    status = "🔴 Risk" if se.margin_pct < 5 else "🟡 Moderate" if se.margin_pct < 20 else "🟢 Excellent"
    scenarios.append({
        "Daily Orders": vol,
        "Monthly Revenue": f"₹{se.revenue:,.0f}",
        "Monthly Profit": f"₹{se.net_profit:,.0f}",
        "Profit Margin": f"{se.margin_pct:.1f}%",
        "Breakeven Delta": f"{vol - se.breakeven_daily} orders/day",
        "Status": status
    })

df_scenarios = pd.DataFrame(scenarios)

# Pandas Styler for Executive Look
def style_status(val):
    if "Excellent" in val: return 'color: #10B981; font-weight: bold;'
    if "Moderate" in val: return 'color: #F59E0B; font-weight: bold;'
    if "Risk" in val: return 'color: #EF4444; font-weight: bold;'
    return ''

styled_df = df_scenarios.style.applymap(style_status, subset=['Status']).set_properties(**{
    'background-color': '#FFFFFF',
    'color': '#0F172A',
    'border-color': '#E2E8F0',
    'padding': '12px',
    'text-align': 'center'
})

st.dataframe(styled_df, use_container_width=True, hide_index=True)

st.markdown("<br><p style='text-align: center; color: #94A3B8; font-size: 12px;'>CONFIDENTIAL & PROPRIETARY. For Internal Strategy Only.</p>", unsafe_allow_html=True)
