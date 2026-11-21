"""Netflix-inspired styling: CSS, Plotly template and card-row helpers."""
from __future__ import annotations

import html

import plotly.graph_objects as go

RED = "#E50914"
NETFLIX_COLORS = ["#E50914", "#F5F5F1", "#B20710", "#831010", "#564D4D", "#B3B3B3"]
TYPE_COLORS = {"Movie": "#E50914", "TV Show": "#F5F5F1"}
RED_SCALE = [[0, "#2B2B2B"], [0.5, "#831010"], [1, "#E50914"]]

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Inter:wght@400;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; }
.block-container { padding-top: 1rem; max-width: 1400px; }

.netflix-logo {
    font-family: 'Bebas Neue', sans-serif; color: #E50914;
    font-size: 2.6rem; letter-spacing: 4px; line-height: 1;
}

.hero {
    background:
        linear-gradient(to right, #141414 25%, rgba(20,20,20,0.15) 100%),
        linear-gradient(to top, #141414 0%, transparent 40%),
        radial-gradient(circle at 80% 20%, #831010 0%, #141414 70%);
    padding: 70px 40px 60px; border-radius: 8px; margin: 10px 0 10px;
}
.hero .tag { color: #E50914; font-weight: 700; letter-spacing: 3px; font-size: 0.8rem; }
.hero h1 {
    font-family: 'Bebas Neue', sans-serif; font-size: 4.2rem; letter-spacing: 2px;
    line-height: 1; margin: 6px 0 14px; color: #fff;
}
.hero p { max-width: 560px; font-size: 1.1rem; color: #E5E5E5; margin: 0; }
.hero .insight { margin-top: 16px; color: #fff; font-weight: 600; }

.row-title { font-size: 1.3rem; font-weight: 700; margin: 26px 0 4px; color: #E5E5E5; }
.card-row {
    display: flex; gap: 14px; overflow-x: auto; padding: 22px 8px 26px;
    scrollbar-width: thin; scrollbar-color: #E50914 #141414;
}
.card {
    min-width: 190px; height: 112px; border-radius: 6px; padding: 12px 14px;
    background: linear-gradient(135deg, #2B2B2B, #1A1A1A);
    display: flex; flex-direction: column; justify-content: flex-end;
    transition: transform .3s ease, background .3s ease; position: relative; flex-shrink: 0;
}
.card:hover { transform: scale(1.12); background: linear-gradient(135deg, #E50914, #831010);
              cursor: pointer; z-index: 5; box-shadow: 0 8px 24px rgba(0,0,0,.6); }
.card .label { font-weight: 700; font-size: 1rem; line-height: 1.15; color: #fff; }
.card .sub { font-size: .78rem; color: #B3B3B3; margin-top: 3px; }
.card:hover .sub { color: #fff; }
.card .rank {
    position: absolute; top: 2px; right: 10px; font-family: 'Bebas Neue', sans-serif;
    font-size: 3.4rem; color: transparent; -webkit-text-stroke: 2px #595959; line-height: 1;
}

.stButton > button, .stDownloadButton > button {
    background-color: #E50914; color: #fff; border: none; font-weight: 600; border-radius: 4px;
}
.stButton > button:hover, .stDownloadButton > button:hover { background-color: #F6121D; color: #fff; }
[data-testid="stMetric"] {
    background: #1F1F1F; padding: 14px 16px; border-radius: 8px; border-left: 4px solid #E50914;
}
[data-testid="stSidebar"] { background-color: #0B0B0B; border-right: 1px solid #222; }
.stTabs [data-baseweb="tab"] { font-weight: 600; }
.stTabs [aria-selected="true"] { color: #E50914; }
.insight { background:#1F1F1F; border-left:4px solid #E50914; padding:12px 16px;
           border-radius:6px; margin-bottom:10px; }
</style>
"""


def style_fig(fig: go.Figure, height: int = 380) -> go.Figure:
    """Apply the dark Netflix look to a Plotly figure."""
    fig.update_layout(
        paper_bgcolor="#141414", plot_bgcolor="#141414", font_color="#E5E5E5",
        height=height, margin=dict(l=10, r=10, t=50, b=10),
        colorway=NETFLIX_COLORS, legend_title_text="",
        title_font=dict(size=16, color="#FFFFFF"),
    )
    fig.update_xaxes(gridcolor="#2B2B2B", zerolinecolor="#2B2B2B")
    fig.update_yaxes(gridcolor="#2B2B2B", zerolinecolor="#2B2B2B")
    return fig


def card_row(title: str, items: list[tuple[str, str]], ranked: bool = False) -> str:
    """HTML for a horizontally scrolling row. items = [(label, sublabel), ...]."""
    cards = []
    for i, (label, sub) in enumerate(items, start=1):
        rank = f'<span class="rank">{i}</span>' if ranked else ""
        cards.append(
            f'<div class="card">{rank}<span class="label">{html.escape(str(label))}</span>'
            f'<span class="sub">{html.escape(str(sub))}</span></div>'
        )
    return f'<div class="row-title">{html.escape(title)}</div><div class="card-row">{"".join(cards)}</div>'