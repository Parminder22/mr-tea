"""
Mr. Tea Khan Market — Launch Financial Simulation Dashboard
A premium BI-style Streamlit app for consultant pitch.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mr. Tea · Khan Market Launch Simulator",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Global CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ---- Import Inter font ---- */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* ---- Reset Streamlit chrome ---- */
#MainMenu, header, footer { visibility: hidden; }
.block-container { padding: 0 2.5rem 2rem 2.5rem; max-width: 100%; }

/* ---- Root tokens ---- */
:root {
    --bg:        #F5F6FA;
    --card:      #FFFFFF;
    --border:    #E8EBF0;
    --text:      #1A1D23;
    --muted:     #6B7280;
    --accent:    #C8963E;          /* warm gold — tea brand */
    --accent2:   #2D6A4F;          /* deep matcha green */
    --accent3:   #7B3F00;          /* deep brown */
    --danger:    #DC2626;
    --warn:      #D97706;
    --ok:        #059669;
    --radius:    14px;
    --shadow:    0 2px 12px rgba(0,0,0,0.06);
    --shadow-hover: 0 6px 24px rgba(0,0,0,0.11);
}

html, body, [class*="css"] { font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); }

/* ---- Sidebar ---- */
[data-testid="stSidebar"] {
    background: #1A1D23 !important;
    border-right: 1px solid #2E3139;
}
[data-testid="stSidebar"] * { color: #E5E7EB !important; }
[data-testid="stSidebar"] .stSlider > div > div > div { background: var(--accent) !important; }
[data-testid="stSidebar"] label { color: #9CA3AF !important; font-size: 0.72rem; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; }
[data-testid="stSidebar"] h2 { color: #FFFFFF !important; font-size: 1.1rem; font-weight: 700; }
[data-testid="stSidebar"] hr { border-color: #2E3139; }

/* ---- KPI cards ---- */
.kpi-row { display: flex; gap: 1rem; margin-bottom: 1.5rem; }
.kpi-card {
    flex: 1;
    background: var(--card);
    border-radius: var(--radius);
    padding: 1.25rem 1.4rem 1.1rem;
    box-shadow: var(--shadow);
    border-top: 3px solid var(--accent);
    transition: box-shadow 0.2s;
    position: relative; overflow: hidden;
}
.kpi-card:hover { box-shadow: var(--shadow-hover); }
.kpi-card.green  { border-top-color: var(--ok); }
.kpi-card.amber  { border-top-color: var(--warn); }
.kpi-card.blue   { border-top-color: #3B82F6; }
.kpi-card.brown  { border-top-color: var(--accent3); }
.kpi-label { font-size: 0.7rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--muted); margin-bottom: 0.45rem; }
.kpi-value { font-size: 1.85rem; font-weight: 800; color: var(--text); line-height: 1; }
.kpi-sub   { font-size: 0.72rem; color: var(--muted); margin-top: 0.4rem; }
.kpi-badge { display:inline-block; padding:2px 8px; border-radius:20px; font-size:0.65rem; font-weight:700; margin-top:0.5rem; }
.badge-ok   { background:#D1FAE5; color:var(--ok); }
.badge-warn { background:#FEF3C7; color:var(--warn); }
.badge-danger { background:#FEE2E2; color:var(--danger); }

/* ---- Section headings ---- */
.section-title {
    font-size: 0.7rem; font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; color: var(--muted);
    margin: 1.8rem 0 0.9rem; padding-bottom: 0.5rem;
    border-bottom: 1px solid var(--border);
}

/* ---- Chart wrapper ---- */
.chart-card {
    background: var(--card);
    border-radius: var(--radius);
    padding: 1.2rem 1.4rem 0.8rem;
    box-shadow: var(--shadow);
    margin-bottom: 1rem;
}
.chart-title { font-size: 0.82rem; font-weight: 700; color: var(--text); margin-bottom: 0.2rem; }
.chart-sub   { font-size: 0.7rem; color: var(--muted); margin-bottom: 0.8rem; }

/* ---- Table ---- */
.styled-table { width:100%; border-collapse:separate; border-spacing:0; font-size:0.8rem; }
.styled-table th { background:#F1F5F9; color:var(--muted); font-size:0.65rem; font-weight:700; letter-spacing:0.07em; text-transform:uppercase; padding:0.6rem 0.9rem; }
.styled-table td { padding:0.65rem 0.9rem; border-bottom:1px solid var(--border); color:var(--text); }
.styled-table tr:last-child td { border-bottom:none; }
.tag { display:inline-block; padding:2px 10px; border-radius:20px; font-size:0.65rem; font-weight:700; }
.tag-green  { background:#D1FAE5; color:#065F46; }
.tag-yellow { background:#FEF3C7; color:#92400E; }
.tag-red    { background:#FEE2E2; color:#991B1B; }

/* ---- Page header ---- */
.page-header {
    display:flex; align-items:center; gap:1rem;
    padding: 1.6rem 0 1.2rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 1.4rem;
}
.page-logo { font-size:1.9rem; }
.page-title { font-size:1.45rem; font-weight:800; color:var(--text); line-height:1; }
.page-tagline { font-size:0.75rem; color:var(--muted); margin-top:3px; }
.header-right { margin-left:auto; text-align:right; }
.header-badge { background:#FEF9EC; border:1px solid #F0D484; color:#92400E; padding:4px 12px; border-radius:20px; font-size:0.7rem; font-weight:700; }

/* ---- Consultant badge ---- */
.consultant-box {
    background: linear-gradient(135deg, #1A1D23 0%, #2D2F36 100%);
    border-radius: var(--radius); padding: 0.9rem 1.2rem;
    color: #E5E7EB; font-size: 0.75rem;
    display:flex; align-items:center; gap:0.8rem;
    margin-bottom:1.4rem;
    border-left: 3px solid var(--accent);
}

</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR — Inputs
# ═══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🧋 Mr. Tea Simulator")
    st.markdown("**Khan Market, New Delhi**")
    st.markdown("---")

    st.markdown("#### 📦 DEMAND & PRICING")
    daily_orders   = st.slider("Daily Orders",           30,  300,  125, 5)
    ticket_size    = st.slider("Avg. Ticket Size (₹)",  250,  600,  400, 10)

    st.markdown("---")
    st.markdown("#### 🧪 COGS PARAMETERS")
    raw_mat        = st.slider("Raw Material / Cup (₹)",  40,  150,  100, 5)
    pkg_cost       = st.slider("Packaging / Cup (₹)",     10,   40,   25, 1)
    wastage_pct    = st.slider("Wastage Buffer (%)",        0,   10,    5, 1)
    royalty_pct    = st.slider("Franchise Royalty (%)",     0,   15,    5, 1)

    st.markdown("---")
    st.markdown("#### 🏢 FIXED OVERHEADS / MONTH")
    rent           = st.slider("Lease / Rent (₹)",     100_000, 400_000, 250_000, 10_000)
    payroll        = st.slider("Staff Payroll (₹)",     30_000, 150_000,  60_000,  5_000)
    utilities      = st.slider("Utilities & Misc (₹)",  10_000,  50_000,  20_000,  2_000)

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.68rem;color:#6B7280;line-height:1.6'>
    🔒 Prepared by <strong style='color:#C8963E'>Launch Consultant</strong><br>
    Hybrid Model: ₹30k base + 10–15% net profit share
    </div>
    """, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# CORE CALCULATIONS
# ═══════════════════════════════════════════════════════════════════════════════
WORKING_DAYS = 26   # operational days per month

def calculate(orders, ticket, rm, pkg, wst_pct, roy_pct, rent_, payroll_, utils_):
    monthly_orders = orders * WORKING_DAYS

    # Revenue
    gross_rev = monthly_orders * ticket

    # Variable costs per cup
    wastage_cost = rm * (wst_pct / 100)
    royalty_per_cup = ticket * (roy_pct / 100)
    variable_per_cup = rm + pkg + wastage_cost + royalty_per_cup
    total_variable = variable_per_cup * monthly_orders

    # Fixed costs
    total_fixed = rent_ + payroll_ + utils_

    # Profit
    net_profit = gross_rev - total_variable - total_fixed
    margin = (net_profit / gross_rev * 100) if gross_rev > 0 else 0

    # Contribution margin per cup
    contribution_per_cup = ticket - variable_per_cup
    
    # Break-even in orders/day
    if contribution_per_cup > 0:
        breakeven_monthly = total_fixed / contribution_per_cup
        breakeven_daily   = breakeven_monthly / WORKING_DAYS
    else:
        breakeven_daily = float('inf')

    return {
        "gross_rev":           gross_rev,
        "net_profit":          net_profit,
        "margin":              margin,
        "breakeven_daily":     breakeven_daily,
        "total_variable":      total_variable,
        "total_fixed":         total_fixed,
        "monthly_orders":      monthly_orders,
        "variable_per_cup":    variable_per_cup,
        "contribution_per_cup":contribution_per_cup,
        "rm_total":            rm * monthly_orders,
        "pkg_total":           pkg * monthly_orders,
        "wastage_total":       wastage_cost * monthly_orders,
        "royalty_total":       royalty_per_cup * monthly_orders,
        "rent":                rent_,
        "payroll":             payroll_,
        "utils":               utils_,
        "wastage_cost":        wastage_cost,
        "royalty_per_cup":     royalty_per_cup,
        "rm":                  rm,
        "pkg":                 pkg,
    }

res = calculate(daily_orders, ticket_size, raw_mat, pkg_cost,
                wastage_pct, royalty_pct, rent, payroll, utilities)

# ── Health Index ──────────────────────────────────────────────────────────────
def health_index(res):
    score = 100
    if res["margin"] < 20:
        score -= (20 - res["margin"]) * 1.5
    be_ratio = res["breakeven_daily"] / daily_orders if daily_orders > 0 else 1
    if be_ratio > 0.8:
        score -= (be_ratio - 0.8) * 100
    if res["net_profit"] < 0:
        score -= 30
    return max(0, min(100, score))

hi_score = health_index(res)

# ═══════════════════════════════════════════════════════════════════════════════
# PAGE HEADER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
  <div class="page-logo">🧋</div>
  <div>
    <div class="page-title">Mr. Tea · Khan Market</div>
    <div class="page-tagline">Launch Financial Simulation · New Delhi Premium Kiosk</div>
  </div>
  <div class="header-right">
    <span class="header-badge">📊 CONSULTANT DECK · CONFIDENTIAL</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="consultant-box">
  <span style="font-size:1.3rem">📋</span>
  <div>
    <strong style='color:#C8963E'>Engagement Model Under Discussion:</strong>&nbsp;
    ₹30,000/mo base retainer + 10–15% net profit share &nbsp;|&nbsp;
    This simulator demonstrates executive-level operational intelligence brought to this partnership.
  </div>
</div>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 1: KPI CARDS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📈 Executive KPIs — Monthly View</div>', unsafe_allow_html=True)

def fmt_inr(v, crore=False):
    if abs(v) >= 1_00_000:
        return f"₹{v/1_00_000:.2f}L"
    return f"₹{v:,.0f}"

margin_color  = "ok" if res["margin"] >= 25 else ("warn" if res["margin"] >= 10 else "danger")
profit_color  = "ok" if res["net_profit"] > 0 else "danger"
be_ratio      = res["breakeven_daily"] / daily_orders if daily_orders > 0 else 1
be_color      = "ok" if be_ratio < 0.6 else ("warn" if be_ratio < 0.8 else "danger")

kpi_html = f"""
<div class="kpi-row">
  <div class="kpi-card brown">
    <div class="kpi-label">Monthly Gross Revenue</div>
    <div class="kpi-value">{fmt_inr(res['gross_rev'])}</div>
    <div class="kpi-sub">{daily_orders} orders × ₹{ticket_size} × {WORKING_DAYS} days</div>
  </div>
  <div class="kpi-card {'green' if res['net_profit']>0 else 'amber'}">
    <div class="kpi-label">Net Operating Profit</div>
    <div class="kpi-value" style="color:{'#059669' if res['net_profit']>0 else '#DC2626'}">{fmt_inr(res['net_profit'])}</div>
    <div class="kpi-sub">After all variable + fixed costs</div>
    <span class="kpi-badge badge-{profit_color}">{'▲ Profitable' if res['net_profit']>0 else '▼ Loss'}</span>
  </div>
  <div class="kpi-card blue">
    <div class="kpi-label">Net Profit Margin</div>
    <div class="kpi-value" style="color:{'#059669' if res['margin']>=20 else ('#D97706' if res['margin']>=10 else '#DC2626')}">{res['margin']:.1f}%</div>
    <div class="kpi-sub">Target: &gt;20% for healthy ops</div>
    <span class="kpi-badge badge-{margin_color}">{'✓ Healthy' if res['margin']>=20 else ('⚠ Moderate' if res['margin']>=10 else '✗ Critical')}</span>
  </div>
  <div class="kpi-card {'green' if be_ratio<0.6 else 'amber'}">
    <div class="kpi-label">Daily Break-even Orders</div>
    <div class="kpi-value">{res['breakeven_daily']:.0f}<span style="font-size:1rem;font-weight:500"> cups</span></div>
    <div class="kpi-sub">{be_ratio*100:.0f}% of your {daily_orders}-cup target</div>
    <span class="kpi-badge badge-{be_color}">{'✓ Comfortable' if be_ratio<0.6 else ('⚠ Tight' if be_ratio<0.8 else '✗ Risky')}</span>
  </div>
</div>
"""
st.markdown(kpi_html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 2: 12-MONTH TRAJECTORY + HEALTH GAUGE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">📅 Growth Trajectory & Business Health</div>', unsafe_allow_html=True)
col1, col2 = st.columns([3, 2])

PLOTLY_CFG  = dict(displayModeBar=False)
CHART_STYLE = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#6B7280", size=11),
    margin=dict(l=10, r=10, t=30, b=10),
)

PALETTE = ["#C8963E", "#2D6A4F", "#3B82F6", "#DC2626", "#7B3F00", "#8B5CF6"]

with col1:
    months = [f"M{i+1}" for i in range(12)]
    rev_list, prof_list = [], []
    orders_m = daily_orders
    for _ in range(12):
        r = calculate(orders_m, ticket_size, raw_mat, pkg_cost,
                      wastage_pct, royalty_pct, rent, payroll, utilities)
        rev_list.append(r["gross_rev"] / 1_00_000)
        prof_list.append(r["net_profit"] / 1_00_000)
        orders_m *= 1.03   # 3% MoM volume growth

    fig_proj = go.Figure()
    fig_proj.add_trace(go.Scatter(
        x=months, y=rev_list, name="Revenue",
        line=dict(color=PALETTE[0], width=2.5),
        fill="tozeroy", fillcolor="rgba(200,150,62,0.08)",
        mode="lines+markers", marker=dict(size=5)
    ))
    fig_proj.add_trace(go.Scatter(
        x=months, y=prof_list, name="Net Profit",
        line=dict(color=PALETTE[1], width=2.5, dash="dash"),
        mode="lines+markers", marker=dict(size=5)
    ))
    fig_proj.add_hline(y=0, line_dash="dot", line_color="#DC2626", line_width=1, opacity=0.5)
    fig_proj.update_layout(
        **CHART_STYLE,
        legend=dict(orientation="h", y=1.15, x=0, bgcolor="rgba(0,0,0,0)"),
        yaxis=dict(tickprefix="₹", ticksuffix="L", gridcolor="#F1F5F9", zeroline=False),
        xaxis=dict(gridcolor="#F1F5F9"),
        height=300,
    )
    st.markdown('<div class="chart-card"><div class="chart-title">12-Month Revenue & Profit Trajectory</div><div class="chart-sub">Assumes 3% month-over-month order volume growth</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_proj, use_container_width=True, config=PLOTLY_CFG)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    hi_color = "#059669" if hi_score >= 70 else ("#D97706" if hi_score >= 40 else "#DC2626")
    hi_label = "Excellent" if hi_score >= 70 else ("Moderate Risk" if hi_score >= 40 else "High Risk")

    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number",
        value=hi_score,
        number=dict(suffix="/100", font=dict(size=28, family="Inter", color=hi_color)),
        gauge=dict(
            axis=dict(range=[0, 100], tickwidth=1, tickcolor="#E5E7EB"),
            bar=dict(color=hi_color, thickness=0.25),
            bgcolor="rgba(0,0,0,0)",
            borderwidth=0,
            steps=[
                dict(range=[0,  40], color="#FEE2E2"),
                dict(range=[40, 70], color="#FEF3C7"),
                dict(range=[70,100], color="#D1FAE5"),
            ],
            threshold=dict(line=dict(color=hi_color, width=3), thickness=0.75, value=hi_score),
        )
    ))
    fig_gauge.update_layout(
        **CHART_STYLE,
        height=250,
        annotations=[dict(
            text=f"<b>{hi_label}</b>",
            x=0.5, y=0.18, showarrow=False,
            font=dict(size=13, color=hi_color, family="Inter"),
            xref="paper", yref="paper"
        )]
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Financial Health Index</div><div class="chart-sub">Composite score: margin quality + break-even safety</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_gauge, use_container_width=True, config=PLOTLY_CFG)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 3: P&L WATERFALL + OPEX DONUT
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">💧 Cost Architecture — Monthly P&L</div>', unsafe_allow_html=True)
col3, col4 = st.columns([3, 2])

with col3:
    wf_labels  = ["Revenue", "Raw Materials", "Packaging", "Wastage", "Royalty", "Rent", "Payroll", "Utilities", "Net Profit"]
    wf_values  = [
        res["gross_rev"],
        -res["rm_total"],
        -res["pkg_total"],
        -res["wastage_total"],
        -res["royalty_total"],
        -res["rent"],
        -res["payroll"],
        -res["utils"],
        res["net_profit"],
    ]
    wf_measure = ["absolute","relative","relative","relative","relative","relative","relative","relative","total"]
    wf_colors  = [PALETTE[0]] + ["#F87171"]*6 + ["#F87171"] + [PALETTE[1] if res["net_profit"]>0 else "#DC2626"]

    fig_wf = go.Figure(go.Waterfall(
        orientation="v",
        measure=wf_measure,
        x=wf_labels,
        y=wf_values,
        connector=dict(line=dict(color="#E5E7EB", width=1, dash="dot")),
        decreasing=dict(marker=dict(color="#FCA5A5", line=dict(color="#EF4444", width=1))),
        increasing=dict(marker=dict(color="#6EE7B7", line=dict(color="#059669", width=1))),
        totals=dict(marker=dict(color=PALETTE[1] if res["net_profit"]>0 else "#DC2626",
                                line=dict(color=PALETTE[1] if res["net_profit"]>0 else "#DC2626", width=1))),
        text=[fmt_inr(v) for v in wf_values],
        textposition="outside",
        textfont=dict(size=9, color="#374151"),
    ))
    fig_wf.update_layout(
        **CHART_STYLE,
        height=340,
        yaxis=dict(tickprefix="₹", gridcolor="#F1F5F9", zeroline=True, zerolinecolor="#E5E7EB"),
        xaxis=dict(tickfont=dict(size=10)),
        showlegend=False,
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Monthly P&L Waterfall</div><div class="chart-sub">Revenue → COGS deductions → Net Profit</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_wf, use_container_width=True, config=PLOTLY_CFG)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    donut_labels = ["Raw Materials", "Packaging", "Wastage", "Royalty", "Rent", "Payroll", "Utilities"]
    donut_values = [
        res["rm_total"], res["pkg_total"], res["wastage_total"], res["royalty_total"],
        res["rent"], res["payroll"], res["utils"]
    ]
    donut_colors = ["#C8963E","#F59E0B","#FCD34D","#7B3F00","#2D6A4F","#3B82F6","#8B5CF6"]

    fig_donut = go.Figure(go.Pie(
        labels=donut_labels,
        values=donut_values,
        hole=0.55,
        marker=dict(colors=donut_colors, line=dict(color="#FFFFFF", width=2)),
        textinfo="percent",
        textfont=dict(size=10),
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    fig_donut.add_annotation(
        text=f"<b>{fmt_inr(sum(donut_values))}</b><br><span style='font-size:10px'>Total Opex</span>",
        x=0.5, y=0.5, showarrow=False, font=dict(size=13, family="Inter", color="#1A1D23"),
        align="center"
    )
    fig_donut.update_layout(
        **CHART_STYLE,
        height=300,
        legend=dict(orientation="v", x=1, y=0.5, font=dict(size=9)),
        showlegend=True,
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Cost Distribution</div><div class="chart-sub">Variable & fixed opex breakdown</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_donut, use_container_width=True, config=PLOTLY_CFG)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 4: SENSITIVITY HEATMAP + PER-CUP UNIT ECONOMICS
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🔬 Deep Unit Economics & Sensitivity</div>', unsafe_allow_html=True)
col5, col6 = st.columns([3, 2])

with col5:
    order_range  = np.arange(max(30, int(daily_orders*0.5)), int(daily_orders*1.5)+1, max(1, int(daily_orders*0.05)))
    ticket_range = np.arange(250, 610, 25)

    z_matrix = np.zeros((len(ticket_range), len(order_range)))
    for i, t in enumerate(ticket_range):
        for j, o in enumerate(order_range):
            r = calculate(o, t, raw_mat, pkg_cost, wastage_pct, royalty_pct, rent, payroll, utilities)
            z_matrix[i, j] = r["net_profit"] / 1_00_000

    fig_heat = go.Figure(go.Heatmap(
        x=order_range,
        y=ticket_range,
        z=z_matrix,
        colorscale=[
            [0.0,  "#DC2626"],
            [0.4,  "#FEF3C7"],
            [0.6,  "#D1FAE5"],
            [1.0,  "#065F46"],
        ],
        colorbar=dict(title="Net Profit (₹L)", tickfont=dict(size=9)),
        hovertemplate="Orders/day: %{x}<br>Ticket: ₹%{y}<br>Profit: ₹%{z:.2f}L<extra></extra>",
        zsmooth="best",
    ))
    # Mark current position
    fig_heat.add_trace(go.Scatter(
        x=[daily_orders], y=[ticket_size],
        mode="markers",
        marker=dict(symbol="x", size=12, color="white", line=dict(color="#1A1D23", width=2)),
        name="Current",
        showlegend=True,
    ))
    fig_heat.update_layout(
        **CHART_STYLE,
        height=320,
        xaxis=dict(title="Daily Orders", gridcolor="rgba(0,0,0,0)"),
        yaxis=dict(title="Avg Ticket Size (₹)", gridcolor="rgba(0,0,0,0)"),
        legend=dict(x=0.01, y=0.99, bgcolor="rgba(0,0,0,0)", font=dict(size=9)),
    )
    st.markdown('<div class="chart-card"><div class="chart-title">Sensitivity Heatmap — Net Profit (₹ Lakh)</div><div class="chart-sub">× marks your current scenario; green = profit zone</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_heat, use_container_width=True, config=PLOTLY_CFG)
    st.markdown('</div>', unsafe_allow_html=True)

with col6:
    cup_labels  = ["Raw Material", "Packaging", "Wastage", "Royalty"]
    cup_values  = [res["rm"], res["pkg"], res["wastage_cost"], res["royalty_per_cup"]]
    contrib     = res["contribution_per_cup"]
    total_cost_cup = sum(cup_values)

    fig_bar = go.Figure()
    colors_bar = ["#C8963E","#F59E0B","#FCD34D","#7B3F00"]
    bottoms = 0
    for label, val, color in zip(cup_labels, cup_values, colors_bar):
        fig_bar.add_trace(go.Bar(
            name=label, x=["Per Cup Economics"], y=[val],
            marker_color=color, width=0.45,
            text=f"₹{val:.0f}", textposition="inside",
            textfont=dict(size=9, color="white"),
        ))
    fig_bar.add_trace(go.Bar(
        name="Contribution Margin", x=["Per Cup Economics"], y=[max(contrib, 0)],
        marker_color="#2D6A4F", width=0.45,
        text=f"₹{contrib:.0f}", textposition="inside",
        textfont=dict(size=9, color="white"),
    ))
    fig_bar.update_layout(
        **CHART_STYLE,
        barmode="stack",
        height=300,
        yaxis=dict(tickprefix="₹", gridcolor="#F1F5F9"),
        legend=dict(orientation="h", y=-0.2, font=dict(size=9), bgcolor="rgba(0,0,0,0)"),
        showlegend=True,
    )
    # Add ticket price reference line
    fig_bar.add_hline(y=ticket_size, line_dash="dot", line_color=PALETTE[0], line_width=2,
                      annotation_text=f"Ticket ₹{ticket_size}", annotation_position="top right",
                      annotation_font_size=9)
    st.markdown('<div class="chart-card"><div class="chart-title">Per-Cup Unit Economics</div><div class="chart-sub">Cost stack vs contribution margin per order</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_bar, use_container_width=True, config=PLOTLY_CFG)
    st.markdown('</div>', unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# ROW 5: SCENARIO STRESS TEST TABLE
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🧪 Volume Stress Test — Scenario Matrix</div>', unsafe_allow_html=True)

scenarios = [50, 75, 100, 125, 150, 175, 200]
rows = []
for o in scenarios:
    r = calculate(o, ticket_size, raw_mat, pkg_cost, wastage_pct, royalty_pct, rent, payroll, utilities)
    be_delta = o - r["breakeven_daily"]
    if r["margin"] >= 22 and r["net_profit"] > 0:
        status = ("Excellent", "green")
    elif r["net_profit"] > 0:
        status = ("Moderate", "yellow")
    else:
        status = ("At Risk", "red")
    rows.append({
        "Daily Orders":    o,
        "Monthly Revenue": fmt_inr(r["gross_rev"]),
        "Monthly Profit":  fmt_inr(r["net_profit"]),
        "Margin":          f"{r['margin']:.1f}%",
        "Break-even Gap":  f"{be_delta:+.0f} orders/day",
        "_status":         status[0],
        "_cls":            status[1],
        "_current":        o == daily_orders,
    })

table_html = """
<div class="chart-card">
<div class="chart-title">Scenario Analysis — What-If Order Volume</div>
<div class="chart-sub">All scenarios use the current sidebar inputs for costs and pricing</div>
<table class="styled-table">
<thead>
<tr>
  <th>Daily Orders</th>
  <th>Monthly Revenue</th>
  <th>Monthly Profit</th>
  <th>Margin</th>
  <th>Break-even Gap</th>
  <th>Status</th>
</tr>
</thead>
<tbody>
"""
for row in rows:
    highlight = "background:#FFFBEB;" if row["_current"] else ""
    current_marker = " 👈" if row["_current"] else ""
    table_html += f"""
<tr style="{highlight}">
  <td><strong>{row['Daily Orders']}{current_marker}</strong></td>
  <td>{row['Monthly Revenue']}</td>
  <td><strong>{row['Monthly Profit']}</strong></td>
  <td>{row['Margin']}</td>
  <td>{row['Break-even Gap']}</td>
  <td><span class="tag tag-{row['_cls']}">{row['_status']}</span></td>
</tr>
"""
table_html += "</tbody></table></div>"
st.markdown(table_html, unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div style='margin-top:2.5rem;padding:1.2rem 1.4rem;background:#1A1D23;border-radius:14px;display:flex;align-items:center;gap:1rem;'>
  <span style='font-size:1.4rem'>🧋</span>
  <div>
    <div style='color:#E5E7EB;font-size:0.78rem;font-weight:700'>Mr. Tea · Khan Market Launch · Financial Intelligence Platform</div>
    <div style='color:#6B7280;font-size:0.68rem;margin-top:3px'>
      Built for internal strategic use · Hybrid Retainer Model Proposal: ₹30k/mo + 10–15% net profit share ·
      All figures are projections; actual results subject to market conditions.
    </div>
  </div>
</div>
""", unsafe_allow_html=True)
