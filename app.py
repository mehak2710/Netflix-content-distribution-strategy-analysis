"""Netflix Content Distribution Strategy Analysis - Streamlit dashboard."""
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from utils.cleaning import MONTH_ORDER, clean, explode
from utils.insights import build_insights, hero_insight
from utils.theme import CSS, NETFLIX_COLORS, RED_SCALE, TYPE_COLORS, card_row, style_fig

st.set_page_config(page_title="Netflix Strategy Analytics", page_icon="🎬", layout="wide")
st.markdown(CSS, unsafe_allow_html=True)

DATA_DIR = Path(__file__).parent / "data"
MAIN_FILE = DATA_DIR / "netflix_titles.csv"


@st.cache_data(show_spinner="Loading catalog...")
def read_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)


@st.cache_data(show_spinner="Cleaning data...")
def prepare(raw: pd.DataFrame) -> pd.DataFrame:
    return clean(raw)


# ----------------------------------------------------------------- data source
st.sidebar.markdown('<div class="netflix-logo">NETFLIX</div>', unsafe_allow_html=True)
st.sidebar.caption("CONTENT STRATEGY ANALYTICS")
upload = st.sidebar.file_uploader("Upload netflix_titles.csv", type="csv")

if upload is not None:
    raw = pd.read_csv(upload)
elif MAIN_FILE.exists():
    raw = read_csv(str(MAIN_FILE))
else:
    st.error("No dataset found. Put netflix_titles.csv in the data/ folder or upload it in the sidebar.")
    st.stop()

df_all = prepare(raw)

# --------------------------------------------------------------------- filters
st.sidebar.markdown("---")
st.sidebar.subheader("Filters")

types = st.sidebar.multiselect("Content type", sorted(df_all["type"].unique()),
                               default=sorted(df_all["type"].unique()))

years = df_all["year_added"].dropna().astype(int)
y_min, y_max = (int(years.min()), int(years.max())) if len(years) else (2008, 2021)
year_range = st.sidebar.slider("Year added", y_min, y_max, (y_min, y_max)) if y_min < y_max else (y_min, y_max)

country_opts = explode(df_all, "countries_list")["countries_list"].value_counts().index.tolist()
sel_countries = st.sidebar.multiselect("Country", country_opts)

genre_opts = explode(df_all, "genres_list")["genres_list"].value_counts().index.tolist()
sel_genres = st.sidebar.multiselect("Genre", genre_opts)

rating_opts = df_all["rating"].value_counts().index.tolist()
sel_ratings = st.sidebar.multiselect("Rating", rating_opts)

mask = df_all["type"].isin(types)
year_mask = df_all["year_added"].between(*year_range)
if (y_min, y_max) == tuple(year_range):
    year_mask |= df_all["year_added"].isna()
mask &= year_mask
if sel_countries:
    mask &= df_all["countries_list"].apply(lambda l: bool(set(l) & set(sel_countries)))
if sel_genres:
    mask &= df_all["genres_list"].apply(lambda l: bool(set(l) & set(sel_genres)))
if sel_ratings:
    mask &= df_all["rating"].isin(sel_ratings)
df = df_all[mask]

st.sidebar.download_button(
    "Download filtered data",
    df.drop(columns=["countries_list", "genres_list"]).to_csv(index=False).encode("utf-8"),
    file_name="netflix_filtered.csv", mime="text/csv",
)

# ------------------------------------------------------------------------ hero
st.markdown('<div class="netflix-logo">NETFLIX ANALYTICS</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="hero"><div class="tag">A DATA ANALYSIS PROJECT</div>'
    '<h1>Content Distribution Strategy</h1>'
    '<p>Explore how Netflix shapes its global catalog across formats, regions, genres and time.</p>'
    f'<div class="insight">{hero_insight(df)}</div></div>',
    unsafe_allow_html=True,
)
if df.empty:
    st.warning("No titles match the current filters.")
    st.stop()

# ------------------------------------------------------------------------ KPIs
genres_x = explode(df, "genres_list")
countries_x = explode(df, "countries_list")
top_country = countries_x["countries_list"].value_counts()

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Total titles", f"{len(df):,}")
k2.metric("Movies", f"{(df['type'] == 'Movie').mean() * 100:.0f}%")
k3.metric("TV shows", f"{(df['type'] == 'TV Show').mean() * 100:.0f}%")
k4.metric("Countries", f"{countries_x['countries_list'].nunique()}")
k5.metric("Top country", top_country.index[0] if len(top_country) else "N/A")

# ------------------------------------------------------------------- card rows
tg = genres_x["genres_list"].value_counts().head(10)
st.markdown(card_row("Top 10 Genres", [(g, f"{c:,} titles") for g, c in tg.items()], ranked=True),
            unsafe_allow_html=True)
tc = top_country.head(10)
st.markdown(card_row("Trending Countries", [(c, f"{n:,} titles") for c, n in tc.items()], ranked=True),
            unsafe_allow_html=True)
recent = df.dropna(subset=["date_added"]).sort_values("date_added", ascending=False).head(12)
st.markdown(card_row("Recently Added",
                     [(r.title, f"{r.type} · {r.date_added:%b %d, %Y}") for r in recent.itertuples()]),
            unsafe_allow_html=True)

# ------------------------------------------------------------------------ tabs
tab_over, tab_geo, tab_genre, tab_dur, tab_search, tab_ins = st.tabs(
    ["Overview", "Geography", "Genres & Ratings", "Duration & Lag", "Title Search", "Strategy Insights"]
)

with tab_over:
    c1, c2 = st.columns([1, 2])
    tc_df = df["type"].value_counts().rename_axis("type").reset_index(name="count")
    fig = px.pie(tc_df, names="type", values="count", hole=0.6, color="type",
                 color_discrete_map=TYPE_COLORS, title="Movies vs TV shows")
    c1.plotly_chart(style_fig(fig), key="pie")

    yearly = df.dropna(subset=["year_added"]).groupby(["year_added", "type"]).size().reset_index(name="count")
    fig = px.bar(yearly, x="year_added", y="count", color="type", color_discrete_map=TYPE_COLORS,
                 title="Titles added per year", labels={"year_added": "Year added", "count": "Titles"})
    c2.plotly_chart(style_fig(fig), key="yearly")

    c3, c4 = st.columns(2)
    share = yearly.pivot(index="year_added", columns="type", values="count").fillna(0)
    if "TV Show" in share.columns:
        share["tv_share"] = share["TV Show"] / share.sum(axis=1) * 100
        fig = px.line(share.reset_index(), x="year_added", y="tv_share", markers=True,
                      title="TV share of additions (%)", labels={"year_added": "Year added", "tv_share": "TV %"})
        fig.update_traces(line_color="#E50914")
        c3.plotly_chart(style_fig(fig), key="tvshare")
    monthly = df.dropna(subset=["month_added"]).groupby("month_added", observed=False).size().reset_index(name="count")
    fig = px.bar(monthly, x="month_added", y="count", title="Seasonality: titles added by month",
                 labels={"month_added": "Month", "count": "Titles"}, category_orders={"month_added": MONTH_ORDER})
    fig.update_traces(marker_color="#E50914")
    c4.plotly_chart(style_fig(fig), key="monthly")

with tab_geo:
    top15 = top_country.head(15).rename_axis("country").reset_index(name="count")
    c1, c2 = st.columns(2)
    fig = px.bar(top15.sort_values("count"), x="count", y="country", orientation="h",
                 title="Top 15 content-producing countries")
    fig.update_traces(marker_color="#E50914")
    c1.plotly_chart(style_fig(fig, 480), key="top15")
    world = top_country.rename_axis("country").reset_index(name="count")
    fig = px.choropleth(world, locations="country", locationmode="country names", color="count",
                        color_continuous_scale=RED_SCALE, title="Global footprint")
    fig.update_geos(bgcolor="#141414", showframe=False, showcountries=True, countrycolor="#2B2B2B",
                    landcolor="#1F1F1F", showocean=False)
    c2.plotly_chart(style_fig(fig, 480), key="map")

    top5 = top_country.head(5).index
    ct = countries_x[countries_x["countries_list"].isin(top5)].dropna(subset=["year_added"])
    ct = ct.groupby(["year_added", "countries_list"]).size().reset_index(name="count")
    fig = px.line(ct, x="year_added", y="count", color="countries_list", markers=True,
                  title="Top 5 countries: titles added per year",
                  labels={"year_added": "Year added", "count": "Titles"})
    st.plotly_chart(style_fig(fig, 400), key="country_trend")

with tab_genre:
    c1, c2 = st.columns(2)
    g15 = genres_x["genres_list"].value_counts().head(15).rename_axis("genre").reset_index(name="count")
    fig = px.bar(g15.sort_values("count"), x="count", y="genre", orientation="h", title="Top 15 genres")
    fig.update_traces(marker_color="#E50914")
    c1.plotly_chart(style_fig(fig, 480), key="genres")
    rt = df["rating"].value_counts().rename_axis("rating").reset_index(name="count")
    fig = px.bar(rt, x="rating", y="count", title="Maturity ratings")
    fig.update_traces(marker_color="#E50914")
    c2.plotly_chart(style_fig(fig, 480), key="ratings")

    top_c8 = top_country.head(8).index
    top_g8 = genres_x["genres_list"].value_counts().head(8).index
    both = df.explode("countries_list").explode("genres_list")
    both = both[both["countries_list"].isin(top_c8) & both["genres_list"].isin(top_g8)]
    both = both.reset_index(drop=True)
    if not both.empty:
        heat = pd.crosstab(both["genres_list"], both["countries_list"])
        fig = px.imshow(heat.values, x=list(heat.columns), y=list(heat.index),
                        color_continuous_scale=RED_SCALE, aspect="auto",
                        title="Genre focus by country (title counts)", text_auto=True)
        st.plotly_chart(style_fig(fig, 420), key="heat")

with tab_dur:
    c1, c2 = st.columns(2)
    movies = df.dropna(subset=["duration_min"])
    if not movies.empty:
        fig = px.histogram(movies, x="duration_min", nbins=40, title="Movie runtime (minutes)")
        fig.update_traces(marker_color="#E50914")
        c1.plotly_chart(style_fig(fig), key="runtime")
    shows = df.dropna(subset=["seasons"])
    if not shows.empty:
        sc = shows["seasons"].astype(int).value_counts().sort_index().rename_axis("seasons").reset_index(name="count")
        fig = px.bar(sc, x="seasons", y="count", title="TV shows by number of seasons")
        fig.update_traces(marker_color="#F5F5F1")
        c2.plotly_chart(style_fig(fig), key="seasons")

    lag = df.dropna(subset=["release_lag"])
    if not lag.empty:
        c3, c4 = st.columns(2)
        fig = px.histogram(lag[lag["release_lag"] <= 30], x="release_lag", nbins=31,
                           title="Release lag: years between release and Netflix addition")
        fig.update_traces(marker_color="#E50914")
        c3.plotly_chart(style_fig(fig), key="lag")
        avg = lag.groupby("year_added")["release_lag"].mean().reset_index()
        fig = px.line(avg, x="year_added", y="release_lag", markers=True,
                      title="Average release lag by year added", labels={"release_lag": "Years"})
        fig.update_traces(line_color="#E50914")
        c4.plotly_chart(style_fig(fig), key="lagtrend")

with tab_search:
    q = st.text_input("Search by title, cast, director or description", placeholder="e.g. Stranger Things")
    res = df
    if q:
        needle = q.strip().lower()
        hay = (df["title"] + " " + df["cast"] + " " + df["director"] + " " + df["description"]).str.lower()
        res = df[hay.str.contains(needle, regex=False)]
    st.caption(f"{len(res):,} titles")
    st.dataframe(
        res[["title", "type", "country", "release_year", "year_added", "rating", "duration", "listed_in"]],
        hide_index=True,
    )

with tab_ins:
    st.subheader("Key takeaways from the current selection")
    for line in build_insights(df):
        st.markdown(f'<div class="insight">{line}</div>', unsafe_allow_html=True)