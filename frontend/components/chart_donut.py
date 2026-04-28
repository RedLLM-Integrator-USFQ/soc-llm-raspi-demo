"""
components/chart_donut.py — Gráfico de dona: Amenazas por severidad
"""
import plotly.graph_objects as go
import streamlit as st

COLORS = {
    "Crítica": "#e53935",
    "Alta":    "#fb8c00",
    "Media":   "#42a5f5",
    "Baja":    "#66bb6a",
}

def render_donut(data: dict, height: int = 300) -> None:
    labels = list(data.keys())
    values = list(data.values())
    colors = [COLORS.get(lbl, "#90a4ae") for lbl in labels]
    legend_labels = [f"{lbl} — {val}" for lbl, val in zip(labels, values)]
    total = sum(values)

    fig = go.Figure(go.Pie(
        labels=legend_labels,
        values=values,
        hole=0.55,
        marker=dict(colors=colors, line=dict(color="#fff", width=2)),
        textinfo="none",
        hovertemplate="<b>%{label}</b><br>%{value} alertas<br>%{percent}<extra></extra>",
        direction="clockwise",
        sort=False,
    ))

    fig.update_layout(
        annotations=[dict(
            text=f"<b>{total}</b><br><span style='font-size:11px;color:#888'>total</span>",
            x=0.5, y=0.5,
            font=dict(size=20, color="#111"),
            showarrow=False,
        )],
        legend=dict(
            orientation="v",
            x= - 0.2, y=0.5,
            yanchor="middle",
            font=dict(size=13, color="#333"),
            bgcolor="rgba(0,0,0,0)",
        ),
        margin=dict(t=80, b=20, l=20, r=20),
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        showlegend=True,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False, "responsive": True})
