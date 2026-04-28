"""pages/1_Dashboard.py — Dashboard principal SOC"""

import json
import streamlit as st
import plotly.graph_objects as go
from pathlib import Path

from components.styles import (
    GLOBAL_CSS, SEV_DOT, ESTADO_CLASS, PRIO_CLASS,
    BAR_COLORS_ATAQUE, EP_COLORS, COMP_COLOR,
)
from components.chart_donut import render_donut

st.set_page_config(page_title="SOC Security Dashboard", page_icon="📊", layout="wide")
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

DATA_PATH = Path(__file__).parent.parent / "data" / "mock_data.json"

@st.cache_data
def load_data():
    with open(DATA_PATH) as f:
        return json.load(f)

d = load_data()

# HEADER
c1, c2 = st.columns([8, 1])
with c1:
    st.markdown("## SOC Security Dashboard")
with c2:
    st.markdown(
        '<div style="padding-top:8px">'
        '<div class="live-badge"><div class="live-dot"></div>LIVE</div>'
        '</div>',
        unsafe_allow_html=True,
    )

# KPIs
st.markdown('<div class="sec">Resumen Operacional</div>', unsafe_allow_html=True)
kpis_cfg = [
    ("Amenazas activas",    str(d["kpis"]["amenazas_activas"]["value"]),    "#e53935",
     "▲ " + d["kpis"]["amenazas_activas"]["delta"],    "#e53935"),
    ("Incidentes abiertos", str(d["kpis"]["incidentes_abiertos"]["value"]), "#e65100",
     "▲ " + d["kpis"]["incidentes_abiertos"]["delta"], "#e65100"),
    ("MTTA (reconoc.)",     f"{d['kpis']['mtta_min']['value']} min",        "#111",
     "▼ " + d["kpis"]["mtta_min"]["delta"],            "#2e7d32"),
    ("MTTR (resolución)",   f"{d['kpis']['mttr_min']['value']} min",        "#111",
     "▲ " + d["kpis"]["mttr_min"]["delta"],            "#e53935"),
]
for col, (lbl, val, vc, delta, dc) in zip(st.columns(4), kpis_cfg):
    with col:
        st.markdown(
            f'<div class="kpi"><div class="kpi-lbl">{lbl}</div>'
            f'<div class="kpi-val" style="color:{vc}">{val}</div>'
            f'<div class="kpi-d" style="color:{dc}">{delta}</div></div>',
            unsafe_allow_html=True,
        )

# AMENAZAS E INCIDENTES
st.markdown('<div class="sec">Amenazas e Incidentes</div>', unsafe_allow_html=True)
col_dona, col_inc = st.columns(2)

with col_dona:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown("**Amenazas por severidad**")
    render_donut(d["amenazas_por_severidad"])
    st.markdown('</div>', unsafe_allow_html=True)

with col_inc:
    rows = "".join([
        f'<tr><td>{inc["id"]}</td><td>{inc["tipo"]}</td>'
        f'<td><span class="badge {ESTADO_CLASS.get(inc["estado"],"b-inv")}">{inc["estado"]}</span></td>'
        f'<td><span class="badge {PRIO_CLASS.get(inc["prioridad"],"b-med")}">{inc["prioridad"]}</span></td></tr>'
        for inc in d["incidentes"]
    ])
    st.markdown(
        f'<div class="panel"><div class="ptitle">Incidentes activos</div>'
        f'<table class="inc-table"><thead><tr>'
        f'<th>ID</th><th>Tipo</th><th>Estado</th><th>Prioridad</th>'
        f'</tr></thead><tbody>{rows}</tbody></table></div>',
        unsafe_allow_html=True,
    )

# TÉCNICAS DE ATAQUE Y RED
st.markdown('<div class="sec">Técnicas de Ataque y Red</div>', unsafe_allow_html=True)
col_tec, col_vol = st.columns(2)

with col_tec:
    max_count = max(t["count"] for t in d["tecnicas_ataque"])
    bars = "".join([
        f'<div class="bar-row"><span style="width:140px;color:#333">{t["nombre"]}</span>'
        f'<div class="bar-bg"><div class="bar-fill" style="width:{int(t["count"]/max_count*100)}%;background:{BAR_COLORS_ATAQUE[i]}"></div></div>'
        f'<span class="bar-cnt">{t["count"]}</span></div>'
        for i, t in enumerate(d["tecnicas_ataque"])
    ])
    st.markdown(
        f'<div class="panel"><div class="ptitle">Top técnicas de ataque (últimas 24h)</div>{bars}</div>',
        unsafe_allow_html=True,
    )

with col_vol:
    vr = d["volumen_red"]
    fig_line = go.Figure(go.Scatter(
        x=vr["horas"], y=vr["eventos"], mode="lines+markers",
        line=dict(color="#e53935", width=2),
        marker=dict(size=6, color="#e53935"),
        fill="tozeroy", fillcolor="rgba(229,57,53,0.07)",
    ))
    fig_line.update_layout(
        title=dict(text="Volumen de eventos de red (últimas 6h)", font=dict(size=14), x=0),
        margin=dict(t=40, b=20, l=20, r=10), height=240,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        yaxis=dict(gridcolor="#f0f0f0", range=[0, 850], tickfont=dict(size=11)),
        xaxis=dict(tickfont=dict(size=11)),
    )
    st.markdown('<div class="panel" style="padding-bottom:4px">', unsafe_allow_html=True)
    st.plotly_chart(fig_line, use_container_width=True, config={"displayModeBar": False})
    st.markdown('</div>', unsafe_allow_html=True)

# UEBA, ENDPOINTS Y CUMPLIMIENTO
st.markdown('<div class="sec">UEBA, Endpoints y Cumplimiento</div>', unsafe_allow_html=True)
col_u, col_ep, col_comp = st.columns(3)

def riesgo_color(r):
    if r >= 80: return "#e53935"
    if r >= 50: return "#fb8c00"
    return "#42a5f5"

with col_u:
    rows_u = "".join([
        f'<div class="user-row"><span>🔴 {u["user"]}</span>'
        f'<span style="color:{riesgo_color(u["riesgo"])};font-weight:600;font-size:12px;">Riesgo {u["riesgo"]}</span></div>'
        for u in d["usuarios_anomalos"]
    ])
    st.markdown(
        f'<div class="panel"><div class="ptitle">Usuarios con comportamiento anómalo</div>{rows_u}</div>',
        unsafe_allow_html=True,
    )

with col_ep:
    total_ep = sum(d["endpoints"].values())
    ep_bars = "".join([
        f'<div class="ep-row"><span class="ep-lbl">{name}</span>'
        f'<div class="ep-bar"><div class="bar-fill" style="width:{int(val/total_ep*100)}%;background:{EP_COLORS[name]}"></div></div>'
        f'<span class="ep-cnt">{val}</span></div>'
        for name, val in d["endpoints"].items()
    ])
    mal_rows = "".join([
        f'<div class="mal-row"><span>{m["nombre"]}</span><span style="color:#888">{m["hosts"]} hosts</span></div>'
        for m in d["malware"]
    ])
    st.markdown(
        f'<div class="panel"><div class="ptitle">Salud de endpoints</div>{ep_bars}'
        f'<div style="font-size:12px;color:#999;margin:14px 0 8px;font-weight:600">Top malware detectado</div>'
        f'{mal_rows}</div>',
        unsafe_allow_html=True,
    )

with col_comp:
    comp_rows = "".join([
        f'<div class="comp-row"><span class="comp-lbl">{c["framework"]}</span>'
        f'<div class="comp-bar"><div class="bar-fill" style="width:{c["pct"]}%;background:{COMP_COLOR(c["pct"])}"></div></div>'
        f'<span class="comp-pct">{c["pct"]}%</span></div>'
        for c in d["cumplimiento"]
    ])
    st.markdown(
        f'<div class="panel"><div class="ptitle">Cumplimiento regulatorio</div>{comp_rows}</div>',
        unsafe_allow_html=True,
    )

# TIMELINE
st.markdown('<div class="sec">Timeline de Eventos Recientes</div>', unsafe_allow_html=True)
tl_html = "".join([
    f'<div style="display:flex;gap:16px;" class="tl-item">'
    f'<span class="tl-time">{e["hora"]}</span>'
    f'<span style="font-size:15px;margin-top:1px">{SEV_DOT.get(e["sev"],"⚪")}</span>'
    f'<div><div class="tl-main">{e["titulo"]}</div><div class="tl-sub">{e["detalle"]}</div></div></div>'
    for e in d["timeline"]
])
st.markdown(f'<div class="panel">{tl_html}</div>', unsafe_allow_html=True)
