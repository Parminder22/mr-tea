import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="Mr. Tea ",
    page_icon="🧋",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

#MainMenu, header, footer, [data-testid="stToolbar"] { visibility: hidden; height: 0; }
.block-container { padding: 1rem 1.5rem 2rem 1.5rem !important; max-width: 100% !important; }
html, body, [class*="css"], * { font-family: 'Inter', sans-serif !important; }
body, .stApp { background: #F0F2F6 !important; }
            

            
/* ── HIDE STREAMLIT BRANDING & FOOTER ── */
#MainMenu { visibility: hidden; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }
div[data-testid="stStatusWidget"] { visibility: hidden; }
            
/* ── NUCLEAR REMOVAL OF ALL BRANDING & PROFILE UI ── */
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
.stDeployButton { display: none !important; }
div[data-testid="stStatusWidget"] { visibility: hidden !important; }

/* Hide the user profile/avatar menu at the top right */
[data-testid="stAppToolbar"] { visibility: hidden !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #FFFFFF !important;
    border-right: 1px solid #E5E7EB !important;
    min-width: 260px !important; max-width: 260px !important;
}

/* ── PERMANENTLY DISABLE SIDEBAR COLLAPSE ── */
[data-testid="stSidebarCollapseButton"], 
[data-testid="collapsedControl"] { 
    display: none !important; 
}

[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSlider label p { color: #374151 !important; font-size: 12px !important; font-weight: 500 !important; }

[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [role="slider"] {
    background: #C8963E !important; border-color: #C8963E !important;
    width: 18px !important; height: 18px !important;
    box-shadow: 0 0 0 3px rgba(200,150,62,0.18) !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] [role="slider"]:hover {
    box-shadow: 0 0 0 6px rgba(200,150,62,0.22) !important;
}
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[data-testid="stSliderTickBarMin"],
[data-testid="stSidebar"] .stSlider [data-baseweb="slider"] div[data-testid="stSliderTickBarMax"] {
    color: #9CA3AF !important; font-size: 10px !important;
}
[data-testid="stSidebar"] .stSlider { margin-bottom: 6px !important; }

.sb-logo { font-size: 20px; font-weight: 800; color: #111827; letter-spacing: -0.5px; margin-bottom: 2px; }
.sb-logo span { color: #C8963E; }
.sb-tagline { font-size: 11px; color: #9CA3AF; margin-bottom: 14px; }
.sb-pill { background: #FEF3C7; color: #92400E; font-size: 10px; font-weight: 700;
           padding: 4px 10px; border-radius: 20px; display: inline-block; margin-bottom: 16px; }
.sb-section { font-size: 9px !important; font-weight: 800 !important; letter-spacing: 0.1em !important;
              text-transform: uppercase !important; color: #9CA3AF !important;
              padding: 10px 0 4px 0 !important; border-top: 1px solid #F3F4F6 !important;
              margin-top: 2px !important; display: block; }

/* ── PAGE HEADER ── */
.page-header { display: flex; align-items: center; margin-bottom: 18px;
               padding-bottom: 14px; border-bottom: 1px solid #E5E7EB; }
.page-header h1 { font-size: 22px !important; font-weight: 800 !important;
                  color: #111827 !important; margin: 0 !important; padding: 0 !important; }
.page-header-sub { font-size: 12px; color: #9CA3AF; margin-top: 2px; }

/* ── KPI CARDS ── */
.kpi-grid { display: grid; grid-template-columns: repeat(5,1fr); gap: 12px; margin-bottom: 18px; }
.kpi-card { background: #FFFFFF; border-radius: 12px; padding: 18px 20px;
            box-shadow: 0 1px 4px rgba(0,0,0,0.06); border: 1px solid #F3F4F6; }
.kpi-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.10); transition: box-shadow 0.18s; }
.kpi-label { font-size: 10px; font-weight: 700; color: #6B7280; text-transform: uppercase;
             letter-spacing: 0.07em; margin-bottom: 10px; }
.kpi-value { font-size: 30px; font-weight: 800; color: #111827; line-height: 1; }
.kpi-value.green { color: #059669; }
.kpi-value.red   { color: #DC2626; }
.kpi-value.amber { color: #D97706; }
.kpi-meta  { font-size: 10px; color: #9CA3AF; margin-top: 6px; }
.kpi-badge { display: inline-block; font-size: 10px; font-weight: 700;
             padding: 2px 8px; border-radius: 20px; margin-top: 8px; }
.b-green  { background: #D1FAE5; color: #065F46; }
.b-yellow { background: #FEF3C7; color: #92400E; }
.b-red    { background: #FEE2E2; color: #991B1B; }
.b-blue   { background: #DBEAFE; color: #1E40AF; }

/* ── SCENARIO TABLE ── */
.sc-wrap { background: #FFFFFF; border-radius: 12px; padding: 18px 20px;
           box-shadow: 0 1px 4px rgba(0,0,0,0.06); border: 1px solid #F3F4F6; margin-bottom: 16px; }
.sc-title { font-size: 13px; font-weight: 700; color: #111827; margin-bottom: 2px; }
.sc-sub   { font-size: 11px; color: #9CA3AF; margin-bottom: 12px; }
.sc-table { width: 100%; border-collapse: collapse; font-size: 12px; }
.sc-table th { font-size: 10px; font-weight: 700; text-transform: uppercase;
               letter-spacing: 0.06em; color: #9CA3AF; padding: 8px 12px;
               text-align: left; border-bottom: 2px solid #F3F4F6; }
.sc-table td { padding: 10px 12px; border-bottom: 1px solid #F9FAFB; color: #374151; }
.sc-table tr:last-child td { border-bottom: none; }
.sc-table tr.hl td { background: #FFFBEB; }
.stag { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 10px; font-weight: 700; }
.s-ex { background: #D1FAE5; color: #065F46; }
.s-mo { background: #FEF3C7; color: #92400E; }
.s-ri { background: #FEE2E2; color: #991B1B; }

/* ── UNIFIED PLOTLY CARDS ── */
[data-testid="stPlotlyChart"] { 
    background: #FFFFFF !important; 
    border-radius: 12px !important; 
    border: 1px solid #F3F4F6 !important; 
    box-shadow: 0 1px 4px rgba(0,0,0,0.06) !important;
    overflow: hidden !important;
    margin-bottom: 16px !important;
    padding-top: 5px !important;
}
[data-testid="stPlotlyChart"] > div { background: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# CONSTANTS & HELPERS
# ══════════════════════════════════════════════════════
DAYS = 26
PLOTLY_CFG = dict(displayModeBar=False)

def base_layout(h, ml=20, mr=20, mt=44, mb=16):
    return dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#374151", size=11),
        height=h,
        margin=dict(l=ml, r=mr, t=mt, b=mb),
    )

def inr(v):
    if abs(v) >= 1_00_000: return f"₹{v/1_00_000:.2f}L"
    if abs(v) >= 1_000:    return f"₹{v/1_000:.1f}k"
    return f"₹{v:.0f}"

def calc(orders, ticket, rm, pkg, wst, roy, rent_, pay_, utils_):
    mo   = orders * DAYS
    rev  = mo * ticket
    wc   = rm * (wst / 100)
    rc   = ticket * (roy / 100)
    vpc  = rm + pkg + wc + rc
    tfx  = rent_ + pay_ + utils_
    np_  = rev - vpc * mo - tfx
    margin = (np_ / rev * 100) if rev > 0 else 0
    cpc  = ticket - vpc
    be   = (tfx / cpc / DAYS) if cpc > 0 else float('inf')
    return dict(rev=rev, np=np_, margin=margin, be=be, tfx=tfx,
                mo=mo, vpc=vpc, cpc=cpc,
                rm_t=rm*mo, pkg_t=pkg*mo, wc_t=wc*mo, rc_t=rc*mo,
                rent=rent_, pay=pay_, utils=utils_, wc=wc, rc=rc, rm=rm, pkg=pkg)

def chart_card(title, subtitle, fig, key=None):
    """Embeds the title into Plotly safely inside the CSS card padding."""
    fig.update_layout(
        title=dict(
            text=f"<span style='font-size:14px; font-weight:800; color:#000000'>{title}</span><br><span style='font-size:11px; color:#6B7280; font-weight:400'>{subtitle}</span>",
            x=0.04, y=0.95, xanchor="left", yanchor="top"
        ),
        margin=dict(t=90) # Pushes chart content down to make clear room for the title
    )
    st.plotly_chart(fig, width="stretch", config=PLOTLY_CFG)

# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div class="sb-logo">Mr. Tea<span>.</span></div>
    <div class="sb-tagline"> · New Delhi</div>
    <div class="sb-pill">📊 Financial Simulator</div>
    """, unsafe_allow_html=True)

    st.markdown('<span class="sb-section">📦 Demand & Pricing</span>', unsafe_allow_html=True)
    daily_orders = st.slider("Daily Orders",          30,  300, 125, 5)
    ticket_size  = st.slider("Avg Ticket Size (₹)",  250,  600, 400, 10)

    st.markdown('<span class="sb-section">🧪 Cost Per Cup</span>', unsafe_allow_html=True)
    raw_mat     = st.slider("Raw Material / Cup (₹)",  40, 150, 100, 5)
    pkg_cost    = st.slider("Packaging / Cup (₹)",     10,  40,  25, 1)
    wastage_pct = st.slider("Wastage Buffer (%)",        0,  10,   5, 1)
    royalty_pct = st.slider("Franchise Royalty (%)",     0,  15,   5, 1)

    st.markdown('<span class="sb-section">🏢 Monthly Fixed Costs</span>', unsafe_allow_html=True)
    rent_k    = st.slider("Rent (₹ thousands)",       100, 400, 250, 10)
    payroll_k = st.slider("Staff Payroll (₹ thou.)",   30, 150,  60,  5)
    utils_k   = st.slider("Utilities & Misc (₹ th.)",  10,  50,  20,  2)

    rent_r = rent_k * 1000;  payroll_r = payroll_k * 1000;  utils_r = utils_k * 1000


# ══════════════════════════════════════════════════════
# COMPUTE
# ══════════════════════════════════════════════════════
r = calc(daily_orders, ticket_size, raw_mat, pkg_cost,
         wastage_pct, royalty_pct, rent_r, payroll_r, utils_r)

be_ratio = r["be"] / daily_orders if daily_orders > 0 else 1
hi = max(0, min(100, 100
    - max(0, 20 - r["margin"]) * 1.5
    - max(0, be_ratio - 0.8) * 100
    - (30 if r["np"] < 0 else 0)))
hi_label = "Excellent" if hi >= 70 else ("Moderate" if hi >= 40 else "High Risk")

# ══════════════════════════════════════════════════════
# PAGE HEADER
# ══════════════════════════════════════════════════════
st.markdown("""
<div class="page-header">
  <div>
    <h1>📊 Mr. Tea Financial Dashboard</h1>
    <div class="page-header-sub">Mr. Tea · New Delhi · Adjust sliders to simulate outcomes live</div>
  </div>
</div>""", unsafe_allow_html=True)



# ══════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════
def pb(s): parts = s.split(" ",1); return parts[0], parts[1]
def kpi(label, value, meta, badge_str, val_class=""):
    bc, bl = pb(badge_str)
    return f"""<div class="kpi-card">
  <div class="kpi-label">{label}</div>
  <div class="kpi-value {val_class}">{value}</div>
  <div class="kpi-meta">{meta}</div>
  <span class="kpi-badge {bc}">{bl}</span>
</div>"""

p_cls = "green" if r["np"]>0 else "red"
m_cls = "green" if r["margin"]>=20 else ("amber" if r["margin"]>=10 else "red")
b_cls = "green" if be_ratio<0.6 else ("amber" if be_ratio<0.8 else "red")
h_cls = "green" if hi>=70 else ("amber" if hi>=40 else "red")
p_b = "b-green ✓ Profitable" if r["np"]>0 else "b-red ▼ Loss"
m_b = "b-green ✓ Healthy" if r["margin"]>=20 else ("b-yellow ⚠ Moderate" if r["margin"]>=10 else "b-red ✗ Critical")
be_b= "b-green ✓ Safe" if be_ratio<0.6 else ("b-yellow ⚠ Tight" if be_ratio<0.8 else "b-red ✗ Risky")
h_b = f"b-green ✓ {hi_label}" if hi>=70 else (f"b-yellow ⚠ {hi_label}" if hi>=40 else f"b-red ✗ {hi_label}")

st.markdown(f"""<div class="kpi-grid">
  {kpi("Monthly Revenue",     inr(r['rev']),  f"{daily_orders} orders × ₹{ticket_size} × {DAYS}d", "b-blue Gross")}
  {kpi("Net Operating Profit",inr(r['np']),   "After all costs & overheads", p_b, p_cls)}
  {kpi("Net Profit Margin",   f"{r['margin']:.1f}%","Target › 20% healthy", m_b, m_cls)}
  {kpi("Daily Break-even",    f"{r['be']:.0f} cups",f"{be_ratio*100:.0f}% of {daily_orders}-cup target", be_b, b_cls)}
  {kpi("Health Index",        f"{hi:.0f}/100","Composite financial score", h_b, h_cls)}
</div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════
# ROW 2 — Trajectory + Donut
# ══════════════════════════════════════════════════════
col1, col2 = st.columns([3, 2])

with col1:
    months = [f"M{i+1}" for i in range(12)]
    rev_l, np_l, o = [], [], daily_orders
    for _ in range(12):
        rr = calc(o, ticket_size, raw_mat, pkg_cost, wastage_pct, royalty_pct, rent_r, payroll_r, utils_r)
        rev_l.append(rr["rev"]/1e5);  np_l.append(rr["np"]/1e5);  o *= 1.03

    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=months, y=rev_l, name="Revenue",
        line=dict(color="#3B82F6", width=2.5), fill="tozeroy",
        fillcolor="rgba(59,130,246,0.07)", mode="lines+markers",
        marker=dict(size=5, color="#3B82F6")))
    fig1.add_trace(go.Scatter(x=months, y=np_l, name="Net Profit",
        line=dict(color="#C8963E", width=2.5), fill="tozeroy",
        fillcolor="rgba(200,150,62,0.07)", mode="lines+markers",
        marker=dict(size=5, color="#C8963E")))
    fig1.add_hline(y=0, line_dash="dot", line_color="#EF4444", line_width=1.5, opacity=0.5)
    fig1.update_layout(**base_layout(250, ml=10, mr=10, mt=48, mb=20),
        yaxis=dict(tickprefix="₹", ticksuffix="L", gridcolor="#F3F4F6",
                   zeroline=False, tickfont=dict(size=10, color="#374151")),
        xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont=dict(size=10, color="#374151")),
        legend=dict(orientation="h", y=1.15, x=0, bgcolor="rgba(0,0,0,0)",
                    font=dict(size=10, color="#374151")))
    chart_card("12-Month Revenue & Profit Trajectory",
               "Assumes 3% month-over-month order volume growth", fig1)

with col2:
    dl = ["Raw Materials","Packaging","Wastage","Royalty","Rent","Payroll","Utilities"]
    dv = [r["rm_t"],r["pkg_t"],r["wc_t"],r["rc_t"],r["rent"],r["pay"],r["utils"]]
    dc = ["#3B82F6","#60A5FA","#93C5FD","#1D4ED8","#C8963E","#F59E0B","#FCD34D"]

    fig2 = go.Figure(go.Pie(labels=dl, values=dv, hole=0.58,
        marker=dict(colors=dc, line=dict(color="#FFFFFF", width=2)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>₹%{value:,.0f} · %{percent}<extra></extra>"))
    fig2.add_annotation(text=f"<b>{inr(sum(dv))}</b><br>Total Cost",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=12, family="Inter", color="#111827"), align="center")
    fig2.update_layout(**base_layout(250, ml=0, mr=0, mt=48, mb=10),
        legend=dict(orientation="v", x=1.01, y=0.5,
                    font=dict(size=9, color="#374151"), bgcolor="rgba(0,0,0,0)"))
    chart_card("Cost Distribution", "Monthly opex breakdown by category", fig2)

# ══════════════════════════════════════════════════════
# ROW 3 — Waterfall + Per-cup
# ══════════════════════════════════════════════════════
col3, col4 = st.columns([3, 2])

with col3:
    wl = ["Revenue","Raw Mat.","Packaging","Wastage","Royalty","Rent","Payroll","Utilities","Net Profit"]
    wv = [r["rev"],-r["rm_t"],-r["pkg_t"],-r["wc_t"],-r["rc_t"],-r["rent"],-r["pay"],-r["utils"],r["np"]]
    wm = ["absolute"]+["relative"]*7+["total"]
    pc = "#C8963E" if r["np"]>0 else "#DC2626"

    fig3 = go.Figure(go.Waterfall(
        orientation="v", measure=wm, x=wl, y=wv,
        connector=dict(line=dict(color="#E5E7EB", width=1, dash="dot")),
        decreasing=dict(marker=dict(color="#93C5FD", line=dict(color="#3B82F6", width=1))),
        increasing=dict(marker=dict(color="#6EE7B7", line=dict(color="#059669", width=1))),
        totals=dict(marker=dict(color=pc, line=dict(color=pc, width=1))),
        text=[inr(v) for v in wv], textposition="outside",
        textfont=dict(size=9, color="#111827")))
    fig3.update_layout(**base_layout(280, ml=10, mr=10, mt=48, mb=20),
        showlegend=False,
        yaxis=dict(tickprefix="₹", gridcolor="#F3F4F6", zeroline=True,
                   zerolinecolor="#E5E7EB", tickfont=dict(size=9, color="#374151")),
        xaxis=dict(tickfont=dict(size=9, color="#374151")))
    chart_card("Monthly P&L Waterfall", "Revenue chipped away cost-by-cost to net profit", fig3)

with col4:
    cc = ["Raw Material","Packaging","Wastage","Royalty","Contribution"]
    cv = [r["rm"], r["pkg"], r["wc"], r["rc"], max(r["cpc"],0)]
    cols4 = ["#3B82F6","#60A5FA","#93C5FD","#1D4ED8","#C8963E"]

    fig4 = go.Figure()
    for lab, val, col in zip(cc, cv, cols4):
        fig4.add_trace(go.Bar(name=lab, x=["Per Cup"], y=[val], marker_color=col,
            text=f"₹{val:.0f}", textposition="inside",
            textfont=dict(size=9, color="#FFFFFF"), width=0.45))
    fig4.add_hline(y=ticket_size, line_dash="dash", line_color="#374151", line_width=1.5,
                   annotation_text=f"Ticket ₹{ticket_size}",
                   annotation_font_size=9, annotation_position="top right")
    fig4.update_layout(**base_layout(280, ml=10, mr=10, mt=48, mb=20),
        barmode="stack",
        yaxis=dict(tickprefix="₹", gridcolor="#F3F4F6", tickfont=dict(size=9, color="#374151")),
        legend=dict(orientation="h", y=-0.15, font=dict(size=9, color="#374151"),
                    bgcolor="rgba(0,0,0,0)"))
    chart_card("Per-Cup Unit Economics", "Cost stack vs contribution margin per order", fig4)

# ══════════════════════════════════════════════════════
# ROW 4 — Heatmap full width
# ══════════════════════════════════════════════════════
or_ = np.arange(max(30, int(daily_orders*0.4)), int(daily_orders*1.7)+1, max(1, int(daily_orders*0.05)))
tr_ = np.arange(250, 620, 25)
Z   = np.zeros((len(tr_), len(or_)))
for i, t in enumerate(tr_):
    for j, o in enumerate(or_):
        rr = calc(o, t, raw_mat, pkg_cost, wastage_pct, royalty_pct, rent_r, payroll_r, utils_r)
        Z[i,j] = rr["np"]/1e5

fig5 = go.Figure(go.Heatmap(
    x=or_, y=tr_, z=Z,
    colorscale=[[0,"#FEE2E2"],[0.45,"#FEF9C3"],[0.55,"#D1FAE5"],[1,"#065F46"]],
    colorbar=dict(title="₹L", tickfont=dict(size=9, color="#374151"), thickness=12),
    hovertemplate="Orders: %{x}/day | Ticket: ₹%{y} | Profit: ₹%{z:.2f}L<extra></extra>",
    zsmooth="best"))
fig5.add_trace(go.Scatter(x=[daily_orders], y=[ticket_size], mode="markers",
    marker=dict(symbol="x-thin", size=14, color="#1A1D23",
                line=dict(color="#1A1D23", width=3)),
    name="Your scenario", showlegend=True))
fig5.update_layout(**base_layout(290, ml=10, mr=70, mt=48, mb=20),
    xaxis=dict(title="Daily Orders", tickfont=dict(size=10, color="#374151"),
               gridcolor="rgba(0,0,0,0)", title_font=dict(color="#374151")),
    yaxis=dict(title="Ticket Size (₹)", tickfont=dict(size=10, color="#374151"),
               gridcolor="rgba(0,0,0,0)", title_font=dict(color="#374151")),
    legend=dict(x=0.01, y=0.99, bgcolor="rgba(0,0,0,0)", font=dict(size=9, color="#374151")))
chart_card("Sensitivity Heatmap — Net Profit (₹ Lakh)",
           "× = your current scenario · green = profit zone · red = loss zone", fig5)

# ══════════════════════════════════════════════════════
# ROW 5 — Scenario table (pure HTML, no chart)
# ══════════════════════════════════════════════════════
rows_html = ""
for o in [50, 75, 100, 125, 150, 175, 200, 250]:
    rr = calc(o, ticket_size, raw_mat, pkg_cost, wastage_pct, royalty_pct, rent_r, payroll_r, utils_r)
    gap = o - rr["be"]
    if rr["margin"]>=22 and rr["np"]>0: stag,scls = "Excellent","s-ex"
    elif rr["np"]>0:                    stag,scls = "Moderate","s-mo"
    else:                               stag,scls = "At Risk","s-ri"
    is_cur = (o == daily_orders)
    pcol = "#059669" if rr["np"]>0 else "#DC2626"
    rows_html += f"""<tr class="{'hl' if is_cur else ''}">
  <td><strong>{o}{'  👈' if is_cur else ''}</strong></td>
  <td>{inr(rr['rev'])}</td>
  <td style="color:{pcol};font-weight:700">{inr(rr['np'])}</td>
  <td>{rr['margin']:.1f}%</td>
  <td>{gap:+.0f} orders/day</td>
  <td>₹{rr['cpc']:.0f}</td>
  <td><span class="stag {scls}">{stag}</span></td>
</tr>"""

st.markdown(f"""
<div class="sc-wrap">
  <div class="sc-title">Volume Stress Test — Scenario Matrix</div>
  <div class="sc-sub">Highlighted row = current simulation · all other inputs held constant</div>
  <table class="sc-table">
    <thead><tr>
      <th>Daily Orders</th><th>Monthly Revenue</th><th>Net Profit</th>
      <th>Margin</th><th>Break-even Gap</th><th>Contrib/Cup</th><th>Status</th>
    </tr></thead>
    <tbody>{rows_html}</tbody>
  </table>
</div>""", unsafe_allow_html=True)

# ── Footer ──
st.markdown("""
<div style="background:#FFFFFF;border-radius:12px;border:1px solid #F3F4F6;
     padding:14px 20px;display:flex;align-items:center;gap:10px;
     box-shadow:0 1px 4px rgba(0,0,0,0.04);margin-top:4px">
  <span style="font-size:16px">🧋</span>
  <span style="font-size:11px;color:#9CA3AF">
    Mr. Tea · Financial Intelligence Platform &nbsp;·&nbsp;
    Engagement: ₹30k/mo retainer + 10–15% net profit share &nbsp;·&nbsp;
    All figures are forward-looking projections
  </span>
</div>""", unsafe_allow_html=True)
