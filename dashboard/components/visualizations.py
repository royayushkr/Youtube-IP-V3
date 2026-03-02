import math
from typing import Any, Dict, Iterable, List, Optional, Sequence

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st


PLOTLY_DARK_TEMPLATE: Dict[str, Any] = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"color": "#B0B0B0", "family": "Inter, system-ui"},
        "xaxis": {
            "gridcolor": "rgba(255,255,255,0.05)",
            "zerolinecolor": "rgba(255,255,255,0.05)",
        },
        "yaxis": {
            "gridcolor": "rgba(255,255,255,0.05)",
            "zerolinecolor": "rgba(255,255,255,0.05)",
        },
        "colorway": [
            "#FF0000",
            "#00D4FF",
            "#00E676",
            "#FFB300",
            "#FF6090",
            "#7C4DFF",
            "#FF9100",
        ],
        "hoverlabel": {
            "bgcolor": "#1A1A2E",
            "font": {"color": "#FFFFFF"},
            "bordercolor": "#FF0000",
        },
    }
}


def _apply_dark_template(fig: go.Figure) -> go.Figure:
    """Apply the shared dark template to a Plotly figure."""
    fig.update_layout(**PLOTLY_DARK_TEMPLATE["layout"])
    return fig


def styled_metric_card(
    label: str,
    value: str,
    delta: Optional[str] = None,
    icon: Optional[str] = None,
    color: Optional[str] = None,
) -> str:
    """Return HTML for a single glassmorphism metric card.

    Leading whitespace is avoided so Markdown does not treat the block
    as an indented code block.
    """
    icon_html = f'<span class="metric-icon">{icon}</span>' if icon else ""
    color_style = f"color:{color};" if color else ""
    delta_class = ""
    if delta:
        if delta.strip().startswith(("+", "▲")):
            delta_class = "positive"
        elif delta.strip().startswith(("-", "▼")):
            delta_class = "negative"
    delta_html = (
        f'<div class="metric-delta {delta_class}">{delta}</div>' if delta else ""
    )
    html = (
        f'<div class="metric-card">'
        f'<div class="metric-label">{label}</div>'
        f'<div class="metric-value" style="{color_style}">'
        f'{icon_html}{value}'
        f'</div>'
        f'{delta_html}'
        f'</div>'
    )
    return html


def kpi_row(metrics: List[Dict[str, Any]]) -> None:
    """Render a row of KPI metric cards.

    Each metric dict: {label, value, delta?, icon?, color?}
    """
    cards_html = "".join(
        styled_metric_card(
            m.get("label", ""),
            str(m.get("value", "")),
            delta=m.get("delta"),
            icon=m.get("icon"),
            color=m.get("color"),
        )
        for m in metrics
    )
    st.markdown(f'<div class="metric-row">{cards_html}</div>', unsafe_allow_html=True)


def section_header(title: str, subtitle: Optional[str] = None, icon: Optional[str] = None) -> None:
    """Render a styled section header with optional subtitle."""
    icon_html = f"<span>{icon}</span>" if icon else ""
    st.markdown(
        f'<div class="yt-section-header">{icon_html}<span>{title}</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="yt-section-underline"></div>', unsafe_allow_html=True)
    if subtitle:
        st.markdown(f"<p style='color:#B0B0B0;font-size:13px;'>{subtitle}</p>", unsafe_allow_html=True)


def animated_counter(value: float, label: str) -> None:
    """Render a simple animated counter using CSS animation."""
    st.markdown(
        f"""
        <div class="fade-in" style="margin-bottom:0.6rem;">
            <div class="metric-label">{label}</div>
            <div class="metric-value" style="font-size:32px;">{value:,}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def plotly_line_chart(
    df: pd.DataFrame,
    x: str,
    y_cols: Sequence[str],
    title: str,
    secondary_y: Optional[Iterable[str]] = None,
) -> go.Figure:
    """Create a multi-line Plotly chart with optional secondary y-axis."""
    secondary_y = set(secondary_y or [])
    if secondary_y:
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        for col in y_cols:
            use_secondary = col in secondary_y
            fig.add_trace(
                go.Scatter(
                    x=df[x],
                    y=df[col],
                    name=col,
                    mode="lines+markers",
                    line={"shape": "spline"},
                ),
                secondary_y=use_secondary,
            )
        fig.update_xaxes(title_text=x)
        fig.update_yaxes(title_text=y_cols[0], secondary_y=False)
        if len(y_cols) > 1:
            fig.update_yaxes(title_text=y_cols[-1], secondary_y=True)
    else:
        fig = go.Figure()
        for col in y_cols:
            fig.add_trace(
                go.Scatter(
                    x=df[x],
                    y=df[col],
                    name=col,
                    mode="lines+markers",
                    line={"shape": "spline"},
                )
            )
        fig.update_xaxes(title_text=x)
        fig.update_yaxes(title_text=", ".join(y_cols))

    fig.update_layout(title=title)
    _apply_dark_template(fig)
    return fig


def plotly_bar_chart(
    df: pd.DataFrame,
    x: str,
    y: str,
    title: str,
    horizontal: bool = False,
) -> go.Figure:
    """Create a bar chart with gradient bars."""
    if horizontal:
        fig = go.Figure(
            go.Bar(
                x=df[y],
                y=df[x],
                orientation="h",
                marker=dict(
                    color=df[y],
                    colorscale="Reds",
                    line=dict(color="rgba(255,255,255,0.4)", width=0.5),
                ),
            )
        )
    else:
        fig = go.Figure(
            go.Bar(
                x=df[x],
                y=df[y],
                marker=dict(
                    color=df[y],
                    colorscale="Reds",
                    line=dict(color="rgba(255,255,255,0.4)", width=0.5),
                ),
            )
        )
    fig.update_layout(title=title)
    _apply_dark_template(fig)
    return fig


def plotly_donut_chart(
    df: pd.DataFrame,
    names: str,
    values: str,
    title: str,
) -> go.Figure:
    """Create a donut chart with center label."""
    fig = px.pie(
        df,
        names=names,
        values=values,
        hole=0.55,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(title=title)
    _apply_dark_template(fig)
    return fig


def plotly_heatmap(
    df: pd.DataFrame,
    x: str,
    y: str,
    z: str,
    title: str,
) -> go.Figure:
    """Create a heatmap from tall-form data with x, y, z columns."""
    pivot = df.pivot(index=y, columns=x, values=z)
    fig = go.Figure(
        data=go.Heatmap(
            z=pivot.values,
            x=pivot.columns,
            y=pivot.index,
            colorscale="RdBu",
            reversescale=True,
            colorbar=dict(title=z),
        )
    )
    fig.update_layout(title=title)
    _apply_dark_template(fig)
    return fig


def plotly_radar_chart(
    categories: Sequence[str],
    series: Dict[str, Sequence[float]],
    title: str,
) -> go.Figure:
    """Create a radar / spider chart for competitor comparison."""
    fig = go.Figure()
    for name, values in series.items():
        vals = list(values)
        if vals and vals[0] != vals[-1]:
            vals.append(vals[0])
        cats = list(categories)
        if cats and cats[0] != cats[-1]:
            cats.append(cats[0])
        fig.add_trace(go.Scatterpolar(r=vals, theta=cats, fill="toself", name=name))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True)), title=title)
    _apply_dark_template(fig)
    return fig


def plotly_gauge_chart(
    value: float,
    title: str,
    max_val: float = 100,
) -> go.Figure:
    """Create a circular gauge for scoring."""
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            gauge={
                "axis": {"range": [0, max_val]},
                "bar": {"color": "#FF0000"},
                "steps": [
                    {"range": [0, max_val * 0.5], "color": "#3e1a1a"},
                    {"range": [max_val * 0.5, max_val * 0.8], "color": "#3b3414"},
                    {"range": [max_val * 0.8, max_val], "color": "#123820"},
                ],
            },
            title={"text": title},
        )
    )
    _apply_dark_template(fig)
    return fig


def plotly_scatter(
    df: pd.DataFrame,
    x: str,
    y: str,
    size: Optional[str],
    color: Optional[str],
    title: str,
) -> go.Figure:
    """Create a bubble scatter plot."""
    fig = px.scatter(
        df,
        x=x,
        y=y,
        size=size if size in df.columns else None,
        color=color if color in df.columns else None,
        hover_data=["channel_title", "video_title"] if "video_title" in df.columns else None,
    )
    fig.update_layout(title=title)
    _apply_dark_template(fig)
    return fig


def plotly_treemap(
    df: pd.DataFrame,
    path: Sequence[str],
    values: str,
    title: str,
) -> go.Figure:
    """Create a treemap for keyword intelligence."""
    fig = px.treemap(df, path=path, values=values)
    fig.update_layout(title=title)
    _apply_dark_template(fig)
    return fig


def plotly_funnel_chart(
    stages: Sequence[str],
    values: Sequence[float],
    title: str,
) -> go.Figure:
    """Create a funnel chart for content pipeline stages."""
    fig = go.Figure(
        go.Funnel(
            y=list(stages),
            x=list(values),
            textinfo="value+percent initial",
        )
    )
    fig.update_layout(title=title)
    _apply_dark_template(fig)
    return fig


def styled_dataframe(
    df: pd.DataFrame,
    title: Optional[str] = None,
    precision: int = 1,
    image_columns: Optional[Sequence[str]] = None,
) -> None:
    """Render a styled dataframe with gradients on numeric columns.

    Args:
        df: DataFrame to render.
        title: Optional title shown above the table.
        precision: Decimal precision for numeric columns.
        image_columns: Optional list of columns that should display images if URLs.
    """
    if df.empty:
        st.info("No rows to display.")
        return

    if title:
        st.markdown(f"**{title}**", unsafe_allow_html=True)

    numeric_cols = df.select_dtypes(include=[np.number]).columns
    styler = df.style.format(precision=precision)
    if len(numeric_cols) > 0:
        styler = styler.background_gradient(
            subset=numeric_cols, cmap="Reds", low=0.0, high=0.6
        )

    # Use Streamlit's native image column config when requested
    column_config: Dict[str, Any] = {}
    if image_columns:
        for col in image_columns:
            if col in df.columns:
                column_config[col] = st.column_config.ImageColumn(col)

    st.dataframe(
        styler,
        use_container_width=True,
        hide_index=True,
        column_config=column_config or None,
    )


def styled_keyword_chips(keywords: Sequence[str]) -> None:
    """Render a set of keywords as styled chips."""
    chips = "".join(f'<span class="keyword-chip">{kw}</span>' for kw in keywords)
    st.markdown(chips, unsafe_allow_html=True)

