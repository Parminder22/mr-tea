"""
Mr. Tea Khan Market — Launch Financial Simulation Dashboard
Clean light theme matching reference design aesthetic.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mr. Tea · Khan Market",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── CSS — strict light theme matching reference images ─────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

/* Hide Streamlit chrome */
#MainMenu, header, footer, [data-testid="stToolbar"] { visibility: hidden; height: 0; }
[data-testid="stSidebar"] { display: none; }
.block-container { padding: 0 !important; max-width: 100% !important; }
section.main > div { padding: 0 !important; }

/* Root */
* { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }
body, .stApp { background: #F0F2F6 !important; }

/* ── Layout wrapper ── */
.dash-root { background: #F0F2F6; min-height: 100vh; padding: 0 28px 32px 28px; }

/* ── Top nav bar ── */
.topbar {
  background: #FFFFFF;
  border-bottom: 1px solid #E8EBF0;
  padding: 0 28px;
  display: flex;
  align-items: center;
  height: 60px;
  margin: 0 -28px 24px -28px;
  gap: 12px;
}
.topbar-logo { font-size: 18px; font-weight: 800; color: #1A1D23; letter-spacing: -0.5px; }
.topbar-logo span { color: #C8963E; }
.topbar-sep { color: #D1D5DB; margin: 0 4px; }
.topbar-right { margin-left: auto; display: flex; align-items: center; gap: 16px; }
.topbar-link { font-size: 13px; color: #6B7280; font-weight: 500; cursor: pointer; }
.topbar-link.active { color: #1A1D23; font-weight: 700; }

/* ── Page title area ── */
.page-title-area { margin-bottom: 20px; }
.page-title { font-size: 22px; font-weight: 700; color: #111827; margin: 0 0 2px 0; }
.page-breadcrumb { font-size: 12px; color: #9CA3AF; }

/* ── Filter bar ── */
.filter-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  background: #FFFFFF;
  border: 1px solid #E8EBF0;
  border-radius: 12px;
  padding: 12px 16px;
  margin-bottom: 20px;
  box-shadow: 0 1px 4px rgba(0,0,0,0.04);
}
.filter-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  background: #F9FAFB;
  border: 1px solid #E5E7EB;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 12px;
  font-weight: 500;
  color: #374151;
  cursor: pointer;
}
.filter-chip-label { font-size: 10px; color: #9CA3AF; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; margin-right: 2px; }
.filter-sep { width: 1px; height: 28px; background: #E5E7EB; margin: 0 4px; }

/* ── KPI Cards ── */
.kpi-card {
  background: #FFFFFF;
  border-radius: 14px;
  padding: 20px 22px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.06);
  border: 1px solid #F0F2F6;
  height: 100%;
}
.kpi-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.09); transition: box-shadow 0.2s; }
.kpi-eyebrow { font-size: 11px; font-weight: 600; color: #9CA3AF; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 12px; }
.kpi-number { font-size: 36px; font-weight: 800; color: #111827; line-height: 1; margin-bottom: 8px; }
.kpi-number.positive { color: #059669; }
.kpi-number.negative { color: #DC2626; }
.kpi-number.neutral  { color: #111827; }
.kpi-sub { font-size: 11px; color: #9CA3AF; margin-top: 6px; }
.kpi-badge { display: inline-block; padding: 2px 8px; border-radius: 20px; font-size: 10px; font-weight: 700; margin-top: 8px; }
.badge-green  { background: #D1FAE5; color: #065F46; }
.badge-yellow { background: #FEF3C7; color: #92400E; }
.badge-red    { background: #FEE2E2; color: #991B1B; }
.badge-blue   { background: #DBEAFE; color: #1E40AF; }

/* ── Chart cards ── */
.chart-card {
  background: #FFFFFF;
  border-radius: 14px;
  padding: 18px 20px 10px 20px;
  box-shadow: 0 1px 6px rgba(0,0,0,0.06);
  border: 1px solid #F0F2F6;
  margin-bottom: 16px;
}
.chart-card-title { font-size: 13px; font-weight: 700; color: #111827; margin-bottom: 2px; }
.chart-card-sub   { font-size: 11px; color: #9CA3AF; margin-bottom: 4px; }

/* ── Scenario table ── */
.sc-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.sc-table th { font-size: 10px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em; color: #9CA3AF; padding: 8px 12px; text-align: left; border-bottom: 1px solid #F0F2F6; }
.sc-table td { padding: 10px 12px; border-bottom: 1px solid #F9FAFB; color: #374151; }
.sc-table tr:last-child td { border-bottom: none; }
.sc-table tr.active-row td { background: #FFFBEB; }
.status-tag { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 10px; font-weight: 700; }
.s-excellent { background: #D1FAE5; color: #065F46; }
.s-moderate  { background: #FEF3C7; color: #92400E; }
.s-risk      { background: #FEE2E2; color: #991B1B; }

/* ── Consultant banner ── */
.consultant-banner {
  background: linear-gradient(90deg, #1A1D23 0%, #2D3748 100%);
  border-radius: 14px;
  padding: 14px 20px;
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 20px;
}
.cb-text-main { font-size: 13px; font-weight: 700; color: #F9FAFB; }
.cb-text-sub  { font-size: 11px; color: #9CA3AF; margin-top: 2px; }
.cb-pill { background: #C8963E; color: white; font-size: 10px; font-weight: 700; padding: 3px 10px; border-radius: 20px; margin-left: auto; white-space: nowrap; }

/* ── Slider row ── */
.slider-section { background: #FFFFFF; border-radius: 14px; padding: 18px 20px; box-shadow: 0 1px 6px rgba(0,0,0,0.06); border: 1px solid #F0F2F6; margin-bottom: 20px; }
.slider-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 8px 24px; }
.section-label { font-size: 10px; font-weight: 700; color: #9CA3AF; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 12px; }

/* Fix streamlit slider track */
.stSlider [data-baseweb="slider"] div[role="slider"] { background: #C8963E !important; border-color: #C8963E !important; }

/* Streamlit columns gap */
[data-testid="column"] { padding: 0 6px !important; }

</style>
""", unsafe_allow_html=True)

WORKING_DAYS = 26
PLOTLY_CFG   = dict(displayModeBar=False)
BASE_LAYOUT  = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#6B7280", size=11),
    margin=dict(l=0, r=0, t=10, b=0),
)

# ════════════════════════════════════════════════════════
# TOP NAV
# ════════════════════════════════════════════════════════
st.markdown("""
<div class="topbar">
  <div class="topbar-logo">Mr. Tea<span>.</span></div>
  <span class="topbar-sep">/</span>
  <span class="topbar-link active">Dashboard</span>
  <span class="topbar-sep">·</span>
  <span class="topbar-link">P&amp;L</span>
  <span class="topbar-sep">·</span>
  <span class="topbar-link">Scenarios</span>
  <span class="topbar-sep">·</span>
  <span class="topbar-link">Unit Economics</span>
  <div class="topbar-right">
    <span style="font-size:12px;color:#9CA3AF;">Khan Market, New Delhi</span>
    <span style="background:#FEF9EC;border:1px solid #F0D484;color:#92400E;padding:3px 10px;border-radius:20px;font-size:10px;font-weight:700;">CONFIDENTIAL</span>
  </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="dash-root">', unsafe_allow_html=True)

# ── Consultant Banner ────────────────────────────────────
st.markdown("""
<div class="consultant-banner">
  <span style="font-size:22px;">🧋</span>
  <div>
    <div class="cb-text-main">Launch Consultant · Financial Intelligence Platform</div>
    <div class="cb-text-sub">Built to demonstrate executive-level operational value — adjust any variable below to simulate real outcomes</div>
  </div>
  <div class="cb-pill">₹30k Base + 10–15% Net Profit Share</div>
</div>
""", unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# INLINE CONTROLS (filter-bar style like image 1)
# ════════════════════════════════════════════════════════
st.markdown("""
<div class="filter-bar">
  <span style="font-size:13px;font-weight:700;color:#111827;">Simulation Controls</span>
  <div class="filter-sep"></div>
  <span style="font-size:11px;color:#9CA3AF;">Drag sliders below · All charts update live</span>
</div>
""", unsafe_allow_html=True)

# ── Sliders in a 5-column grid (inline, not sidebar) ─────
st.markdown('<div class="slider-section"><div class="section-label">📦 Demand & Pricing</div>', unsafe_allow_html=True)
c1, c2, c3, c4, c5 = st.columns(5)
with c1: daily_orders = st.slider("Daily Orders",          30,  300, 125, 5)
with c2: ticket_size  = st.slider("Avg Ticket Size (₹)",  250, 600, 400, 10)
with c3: raw_mat      = st.slider("Raw Material/Cup (₹)",  40, 150, 100, 5)
with c4: pkg_cost     = st.slider("Packaging/Cup (₹)",     10,  40,  25, 1)
with c5: wastage_pct  = st.slider("Wastage %",              0,  10,   5, 1)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="slider-section" style="margin-top:-8px;"><div class="section-label">🏢 Fixed Overheads / Month</div>', unsafe_allow_html=True)
c6, c7, c8, c9, c10 = st.columns(5)
with c6:  royalty_pct = st.slider("Franchise Royalty %",     0,  15,   5, 1)
with c7:  rent        = st.slider("Rent (₹ '000s)",        100, 400, 250, 10)
with c8:  payroll     = st.slider("Payroll (₹ '000s)",      30, 150,  60,  5)
with c9:  utilities   = st.slider("Utilities (₹ '000s)",    10,  50,  20,  2)
with c10: st.markdown('<div style="padding-top:28px;font-size:11px;color:#9CA3AF;">All amounts in ₹ thousands</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# Convert slider values to actual rupees
rent_r     = rent     * 1_000
payroll_r  = payroll  * 1_000
utilities_r= utilities* 1_000

# ════════════════════════════════════════════════════════
# CORE CALCULATIONS
# ════════════════════════════════════════════════════════
def calculate(orders, ticket, rm, pkg, wst_pct, roy_pct, rent_, payroll_, utils_):
    monthly_orders   = orders * WORKING_DAYS
    gross_rev        = monthly_orders * ticket
    wastage_cost     = rm * (wst_pct / 100)
    royalty_per_cup  = ticket * (roy_pct / 100)
    var_per_cup      = rm + pkg + wastage_cost + royalty_per_cup
    total_variable   = var_per_cup * monthly_orders
    total_fixed      = rent_ + payroll_ + utils_
    net_profit       = gross_rev - total_variable - total_fixed
    margin           = (net_profit / gross_rev * 100) if gross_rev > 0 else 0
    contrib_per_cup  = ticket - var_per_cup
    breakeven_daily  = (total_fixed / contrib_per_cup / WORKING_DAYS) if contrib_per_cup > 0 else float('inf')
    return dict(
        gross_rev=gross_rev, net_profit=net_profit, margin=margin,
        breakeven_daily=breakeven_daily, total_fixed=total_fixed,
        monthly_orders=monthly_orders, var_per_cup=var_per_cup,
        contrib_per_cup=contrib_per_cup,
        rm_total=rm*monthly_orders, pkg_total=pkg*monthly_orders,
        wastage_total=wastage_cost*monthly_orders,
        royalty_total=royalty_per_cup*monthly_orders,
        rent=rent_, payroll=payroll_, utils=utils_,
        wastage_cost=wastage_cost, royalty_per_cup=royalty_per_cup,
        rm=rm, pkg=pkg,
    )

res = calculate(daily_orders, ticket_size, raw_mat, pkg_cost,
                wastage_pct, royalty_pct, rent_r, payroll_r, utilities_r)

def fmt_inr(v):
    if abs(v) >= 1_00_000: return f"₹{v/1_00_000:.2f}L"
    if abs(v) >= 1_000:    return f"₹{v/1_000:.1f}k"
    return f"₹{v:.0f}"

be_ratio   = res["breakeven_daily"] / daily_orders if daily_orders > 0 else 1
hi_score   = max(0, min(100, 100
               - (max(0, 20 - res["margin"]) * 1.5)
               - (max(0, be_ratio - 0.8) * 100)
               - (30 if res["net_profit"] < 0 else 0)))
hi_label   = "Excellent" if hi_score >= 70 else ("Moderate" if hi_score >= 40 else "High Risk")
hi_color   = "#059669"   if hi_score >= 70 else ("#D97706" if hi_score >= 40 else "#DC2626")

# ════════════════════════════════════════════════════════
# ROW 1 — KPI CARDS (4 wide + gauge)
# ════════════════════════════════════════════════════════
st.markdown('<div style="height:4px"></div>', unsafe_allow_html=True)
k1, k2, k3, k4, k5 = st.columns([1, 1, 1, 1, 1])

margin_cls  = "positive" if res["margin"] >= 20 else ("neutral" if res["margin"] >= 10 else "negative")
profit_cls  = "positive" if res["net_profit"] > 0 else "negative"
profit_badge= "badge-green" if res["net_profit"]>0 else "badge-red"
margin_badge= "badge-green" if res["margin"]>=20 else ("badge-yellow" if res["margin"]>=10 else "badge-red")
be_badge    = "badge-green" if be_ratio<0.6 else ("badge-yellow" if be_ratio<0.8 else "badge-red")

with k1:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-eyebrow">Monthly Revenue</div>
      <div class="kpi-number neutral">{fmt_inr(res['gross_rev'])}</div>
      <div class="kpi-sub">{daily_orders} orders × ₹{ticket_size} × {WORKING_DAYS}d</div>
      <span class="kpi-badge badge-blue">Gross</span>
    </div>""", unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-eyebrow">Net Operating Profit</div>
      <div class="kpi-number {profit_cls}">{fmt_inr(res['net_profit'])}</div>
      <div class="kpi-sub">After all costs & overheads</div>
      <span class="kpi-badge {profit_badge}">{'▲ Profitable' if res['net_profit']>0 else '▼ Loss'}</span>
    </div>""", unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-eyebrow">Net Margin</div>
      <div class="kpi-number {margin_cls}">{res['margin']:.1f}%</div>
      <div class="kpi-sub">Target › 20% for healthy ops</div>
      <span class="kpi-badge {margin_badge}">{'✓ Healthy' if res['margin']>=20 else ('⚠ Moderate' if res['margin']>=10 else '✗ Critical')}</span>
    </div>""", unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-eyebrow">Daily Break-even</div>
      <div class="kpi-number neutral">{res['breakeven_daily']:.0f} <span style="font-size:18px;font-weight:500;color:#6B7280">cups</span></div>
      <div class="kpi-sub">{be_ratio*100:.0f}% of your {daily_orders}-cup target</div>
      <span class="kpi-badge {be_badge}">{'✓ Safe' if be_ratio<0.6 else ('⚠ Tight' if be_ratio<0.8 else '✗ Risky')}</span>
    </div>""", unsafe_allow_html=True)

with k5:
    st.markdown(f"""
    <div class="kpi-card">
      <div class="kpi-eyebrow">Health Index</div>
      <div class="kpi-number" style="color:{hi_color}">{hi_score:.0f}<span style="font-size:18px;font-weight:500;color:#9CA3AF">/100</span></div>
      <div class="kpi-sub">Composite financial score</div>
      <span class="kpi-badge {'badge-green' if hi_score>=70 else ('badge-yellow' if hi_score>=40 else 'badge-red')}">{hi_label}</span>
    </div>""", unsafe_allow_html=True)

st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# ROW 2 — 12-month trajectory (wide) + donut (narrow)
# ════════════════════════════════════════════════════════
r2a, r2b = st.columns([3, 2])

with r2a:
    months = [f"M{i+1}" for i in range(12)]
    rev_l, prof_l = [], []
    o = daily_orders
    for _ in range(12):
        r = calculate(o, ticket_size, raw_mat, pkg_cost, wastage_pct, royalty_pct, rent_r, payroll_r, utilities_r)
        rev_l.append(r["gross_rev"] / 1_00_000)
        prof_l.append(r["net_profit"] / 1_00_000)
        o *= 1.03

    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(
        x=months, y=rev_l, name="Revenue (₹L)",
        line=dict(color="#3B82F6", width=2.5),
        fill="tozeroy", fillcolor="rgba(59,130,246,0.07)",
        mode="lines+markers", marker=dict(size=5, color="#3B82F6")
    ))
    fig_line.add_trace(go.Scatter(
        x=months, y=prof_l, name="Net Profit (₹L)",
        line=dict(color="#C8963E", width=2.5),
        fill="tozeroy", fillcolor="rgba(200,150,62,0.07)",
        mode="lines+markers", marker=dict(size=5, color="#C8963E")
    ))
    fig_line.add_hline(y=0, line_dash="dot", line_color="#EF4444", line_width=1.5, opacity=0.5)
    fig_line.update_layout(**BASE_LAYOUT,
        height=230, margin=dict(l=0,r=0,t=20,b=0),
        yaxis=dict(tickprefix="₹", ticksuffix="L", gridcolor="#F3F4F6", zeroline=False, tickfont=dict(size=10)),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10)),
        legend=dict(orientation="h", y=1.18, x=0, bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
    )
    st.markdown('<div class="chart-card"><div class="chart-card-title">Revenue & Profit — 12-Month Trajectory</div><div class="chart-card-sub">Simulates 3% month-over-month order volume growth from current inputs</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_line, use_container_width=True, config=PLOTLY_CFG)
    st.markdown('</div>', unsafe_allow_html=True)

with r2b:
    # Donut — cost breakdown
    donut_labels = ["Raw Materials", "Packaging", "Wastage", "Royalty", "Rent", "Payroll", "Utilities"]
    donut_values = [res["rm_total"], res["pkg_total"], res["wastage_total"],
                    res["royalty_total"], res["rent"], res["payroll"], res["utils"]]
    donut_colors = ["#3B82F6","#60A5FA","#93C5FD","#1D4ED8","#C8963E","#F59E0B","#FCD34D"]

    fig_donut = go.Figure(go.Pie(
        labels=donut_labels, values=donut_values, hole=0.6,
        marker=dict(colors=donut_colors, line=dict(color="#FFFFFF", width=2)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} (%{percent})<extra></extra>",
    ))
    fig_donut.add_annotation(
        text=f"<b>{fmt_inr(sum(donut_values))}</b><br><span style='font-size:9px'>Total Cost</span>",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=12, family="Inter", color="#111827"), align="center"
    )
    fig_donut.update_layout(**BASE_LAYOUT,
        height=230, margin=dict(l=0,r=0,t=20,b=0),
        legend=dict(orientation="v", x=1.0, y=0.5, font=dict(size=9), bgcolor="rgba(0,0,0,0)"),
    )
    st.markdown('<div class="chart-card"><div class="chart-card-title">Cost Distribution</div><div class="chart-card-sub">Monthly opex breakdown by category</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_donut, use_container_width=True, config=PLOTLY_CFG)
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# ROW 3 — Waterfall (wide) + Per-cup bar (narrow)
# ════════════════════════════════════════════════════════
r3a, r3b = st.columns([3, 2])

with r3a:
    wf_x = ["Revenue","Raw Mat.","Packaging","Wastage","Royalty","Rent","Payroll","Utilities","Net Profit"]
    wf_y = [res["gross_rev"], -res["rm_total"], -res["pkg_total"], -res["wastage_total"],
            -res["royalty_total"], -res["rent"], -res["payroll"], -res["utils"], res["net_profit"]]
    wf_m = ["absolute","relative","relative","relative","relative","relative","relative","relative","total"]

    fig_wf = go.Figure(go.Waterfall(
        orientation="v", measure=wf_m, x=wf_x, y=wf_y,
        connector=dict(line=dict(color="#E5E7EB", width=1, dash="dot")),
        decreasing=dict(marker=dict(color="#93C5FD", line=dict(color="#3B82F6", width=1))),
        increasing=dict(marker=dict(color="#6EE7B7", line=dict(color="#059669", width=1))),
        totals=dict(marker=dict(color="#C8963E" if res["net_profit"]>0 else "#EF4444",
                                line=dict(color="#C8963E" if res["net_profit"]>0 else "#EF4444",width=1))),
        text=[fmt_inr(v) for v in wf_y], textposition="outside",
        textfont=dict(size=9, color="#374151"),
    ))
    fig_wf.update_layout(**BASE_LAYOUT,
        height=260, margin=dict(l=0,r=0,t=20,b=0),
        yaxis=dict(tickprefix="₹", gridcolor="#F3F4F6", zeroline=True,
                   zerolinecolor="#E5E7EB", tickfont=dict(size=9)),
        xaxis=dict(tickfont=dict(size=9)),
        showlegend=False,
    )
    st.markdown('<div class="chart-card"><div class="chart-card-title">Monthly P&L Waterfall</div><div class="chart-card-sub">Revenue chipped away cost-by-cost down to net profit</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_wf, use_container_width=True, config=PLOTLY_CFG)
    st.markdown('</div>', unsafe_allow_html=True)

with r3b:
    # Per-cup unit economics stacked bar
    cup_cats   = ["Raw Material","Packaging","Wastage","Royalty","Contribution"]
    cup_vals   = [res["rm"], res["pkg"], res["wastage_cost"], res["royalty_per_cup"],
                  max(res["contrib_per_cup"], 0)]
    cup_colors = ["#3B82F6","#60A5FA","#93C5FD","#1D4ED8","#C8963E"]

    fig_cup = go.Figure()
    for label, val, color in zip(cup_cats, cup_vals, cup_colors):
        fig_cup.add_trace(go.Bar(
            name=label, x=["Per Cup"], y=[val],
            marker_color=color,
            text=f"₹{val:.0f}", textposition="inside",
            textfont=dict(size=9, color="white"), width=0.4,
        ))
    fig_cup.add_hline(y=ticket_size, line_dash="dash", line_color="#374151", line_width=1.5,
                      annotation_text=f"Ticket ₹{ticket_size}",
                      annotation_font_size=9, annotation_position="top right")
    fig_cup.update_layout(**BASE_LAYOUT,
        barmode="stack", height=260, margin=dict(l=0,r=0,t=20,b=0),
        yaxis=dict(tickprefix="₹", gridcolor="#F3F4F6", tickfont=dict(size=9)),
        legend=dict(orientation="h", y=-0.12, font=dict(size=8), bgcolor="rgba(0,0,0,0)"),
    )
    st.markdown('<div class="chart-card"><div class="chart-card-title">Per-Cup Unit Economics</div><div class="chart-card-sub">Cost stack vs contribution margin per order</div>', unsafe_allow_html=True)
    st.plotly_chart(fig_cup, use_container_width=True, config=PLOTLY_CFG)
    st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# ROW 4 — Sensitivity Heatmap (full width)
# ════════════════════════════════════════════════════════
st.markdown('<div class="chart-card"><div class="chart-card-title">Sensitivity Heatmap — Net Profit (₹ Lakh)</div><div class="chart-card-sub">× marks your current scenario · Green = profit zone · Red = loss zone</div>', unsafe_allow_html=True)

order_range  = np.arange(max(30, int(daily_orders*0.4)), int(daily_orders*1.6)+1, max(1, int(daily_orders*0.04)))
ticket_range = np.arange(250, 610, 20)
z_matrix     = np.zeros((len(ticket_range), len(order_range)))
for i, t in enumerate(ticket_range):
    for j, o in enumerate(order_range):
        r = calculate(o, t, raw_mat, pkg_cost, wastage_pct, royalty_pct, rent_r, payroll_r, utilities_r)
        z_matrix[i, j] = r["net_profit"] / 1_00_000

fig_heat = go.Figure(go.Heatmap(
    x=order_range, y=ticket_range, z=z_matrix,
    colorscale=[[0,"#FEE2E2"],[0.45,"#FEF9C3"],[0.55,"#D1FAE5"],[1,"#065F46"]],
    colorbar=dict(title="₹L profit", tickfont=dict(size=9), thickness=12),
    hovertemplate="Orders: %{x}/day<br>Ticket: ₹%{y}<br>Net Profit: ₹%{z:.2f}L<extra></extra>",
    zsmooth="best",
))
fig_heat.add_trace(go.Scatter(
    x=[daily_orders], y=[ticket_size], mode="markers",
    marker=dict(symbol="x-thin", size=14, color="white",
                line=dict(color="#1A1D23", width=3)),
    name="Current", showlegend=True,
))
fig_heat.update_layout(**BASE_LAYOUT,
    height=280, margin=dict(l=0, r=60, t=20, b=0),
    xaxis=dict(title="Daily Orders", tickfont=dict(size=10), gridcolor="rgba(0,0,0,0)"),
    yaxis=dict(title="Ticket Size (₹)", tickfont=dict(size=10), gridcolor="rgba(0,0,0,0)"),
    legend=dict(x=0.01, y=0.99, bgcolor="rgba(0,0,0,0)", font=dict(size=9)),
)
st.plotly_chart(fig_heat, use_container_width=True, config=PLOTLY_CFG)
st.markdown('</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════
# ROW 5 — Scenario Stress Test Table
# ════════════════════════════════════════════════════════
st.markdown('<div class="chart-card"><div class="chart-card-title">Volume Stress Test — Scenario Matrix</div><div class="chart-card-sub">How does profitability change at different daily order volumes?</div>', unsafe_allow_html=True)

scenarios = [50, 75, 100, 125, 150, 175, 200, 250]
table_html = """
<table class="sc-table">
<thead><tr>
  <th>Daily Orders</th><th>Monthly Revenue</th><th>Monthly Profit</th>
  <th>Margin %</th><th>Break-even Gap</th><th>Contrib/Cup</th><th>Status</th>
</tr></thead><tbody>
"""
for o in scenarios:
    r = calculate(o, ticket_size, raw_mat, pkg_cost, wastage_pct, royalty_pct, rent_r, payroll_r, utilities_r)
    gap = o - r["breakeven_daily"]
    if r["margin"] >= 22 and r["net_profit"] > 0:
        stag, scls = "Excellent", "s-excellent"
    elif r["net_profit"] > 0:
        stag, scls = "Moderate", "s-moderate"
    else:
        stag, scls = "At Risk", "s-risk"
    is_current = o == daily_orders
    row_cls = "active-row" if is_current else ""
    marker  = " 👈" if is_current else ""
    profit_style = f"color:{'#059669' if r['net_profit']>0 else '#DC2626'};font-weight:700"
    table_html += f"""
<tr class="{row_cls}">
  <td><strong>{o}{marker}</strong></td>
  <td>{fmt_inr(r['gross_rev'])}</td>
  <td style="{profit_style}">{fmt_inr(r['net_profit'])}</td>
  <td>{r['margin']:.1f}%</td>
  <td>{gap:+.0f} orders/day</td>
  <td>₹{r['contrib_per_cup']:.0f}</td>
  <td><span class="status-tag {scls}">{stag}</span></td>
</tr>"""
table_html += "</tbody></table>"
st.markdown(table_html, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ── Footer ───────────────────────────────────────────────
st.markdown("""
<div style="margin-top:8px;padding:14px 20px;background:#FFFFFF;border-radius:14px;
     border:1px solid #F0F2F6;display:flex;align-items:center;gap:12px;
     box-shadow:0 1px 6px rgba(0,0,0,0.04);">
  <span style="font-size:16px">🧋</span>
  <span style="font-size:11px;color:#9CA3AF;">
    Mr. Tea · Khan Market Launch · Financial Intelligence Platform &nbsp;·&nbsp;
    Consultant engagement model: ₹30k/mo retainer + 10–15% net profit share &nbsp;·&nbsp;
    All figures are forward-looking projections
  </span>
</div>
</div>
""", unsafe_allow_html=True)
