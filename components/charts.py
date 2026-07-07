"""Gráficos padronizados com a identidade Physicscool (Plotly)."""
from __future__ import annotations

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

CYAN, INDIGO, PHOTON, ION, QUARK = "#22D3EE", "#818CF8", "#FBBF24", "#34D399", "#FB7185"
PALETTE = [CYAN, INDIGO, PHOTON, ION, QUARK, "#A78BFA", "#38BDF8", "#FB923C"]

_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Inter", color="#94A3B8"),
    margin=dict(l=10, r=10, t=44, b=10),
)


def _style(fig: go.Figure, title: str) -> go.Figure:
    fig.update_layout(title=dict(text=title, font=dict(family="Space Grotesk", size=16, color="#E2E8F0")),
                      **_LAYOUT)
    fig.update_xaxes(gridcolor="rgba(255,255,255,.06)")
    fig.update_yaxes(gridcolor="rgba(255,255,255,.06)")
    return fig


def bar(df: pd.DataFrame, x: str, y: str, title: str, color: str = CYAN) -> go.Figure:
    fig = px.bar(df, x=x, y=y, color_discrete_sequence=[color])
    fig.update_traces(marker_line_width=0, marker=dict(cornerradius=8))
    return _style(fig, title)


def pie(labels: list, values: list, title: str) -> go.Figure:
    fig = go.Figure(go.Pie(labels=labels, values=values, hole=.62,
                           marker=dict(colors=PALETTE, line=dict(width=0))))
    fig.update_traces(textinfo="label+percent")
    return _style(fig, title)


def radar(categories: list[str], values: list[float], title: str) -> go.Figure:
    fig = go.Figure(go.Scatterpolar(r=values + values[:1], theta=categories + categories[:1],
                                    fill="toself", line=dict(color=CYAN),
                                    fillcolor="rgba(34,211,238,.18)"))
    fig.update_layout(polar=dict(bgcolor="rgba(0,0,0,0)",
                                 radialaxis=dict(range=[0, 100], gridcolor="rgba(255,255,255,.08)"),
                                 angularaxis=dict(gridcolor="rgba(255,255,255,.08)")))
    return _style(fig, title)


def line(df: pd.DataFrame, x: str, y: str, title: str, color: str = INDIGO) -> go.Figure:
    fig = px.line(df, x=x, y=y, markers=True, color_discrete_sequence=[color])
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    return _style(fig, title)
