"""Auto-generated strategy insights from the (filtered) catalog."""
from __future__ import annotations

import pandas as pd

from utils.cleaning import explode


def _top_country(df: pd.DataFrame) -> str:
    c = explode(df, "countries_list")["countries_list"].value_counts()
    return c.index[0] if len(c) else "N/A"


def hero_insight(df: pd.DataFrame) -> str:
    if df.empty:
        return "No titles match the current filters."
    movies = (df["type"] == "Movie").mean() * 100
    return (
        f"{movies:.0f}% of the catalog is movies, {100 - movies:.0f}% is TV shows, "
        f"and {_top_country(df)} leads production."
    )


def build_insights(df: pd.DataFrame) -> list[str]:
    """Return markdown bullet strings summarising the strategy story."""
    out: list[str] = []
    if df.empty:
        return out

    n = len(df)
    movies = (df["type"] == "Movie").mean() * 100
    out.append(
        f"**Format mix:** movies make up {movies:.0f}% of the catalog and TV shows "
        f"{100 - movies:.0f}% across {n:,} titles."
    )

    dated = df.dropna(subset=["year_added"])
    sizes = dated.groupby("year_added").size()
    if len(sizes):
        peak = int(sizes.idxmax())
        out.append(f"**Peak acquisition year:** {peak}, with {int(sizes.max()):,} titles added.")
        tv_share = dated.groupby("year_added")["type"].apply(lambda s: (s == "TV Show").mean() * 100)
        valid = tv_share[sizes >= 20]
        if len(valid) >= 2:
            direction = "grew" if valid.iloc[-1] > valid.iloc[0] else "shrank"
            out.append(
                f"**Shift in format:** the TV share of additions {direction} from "
                f"{valid.iloc[0]:.0f}% in {int(valid.index[0])} to "
                f"{valid.iloc[-1]:.0f}% in {int(valid.index[-1])}."
            )

    countries = explode(df, "countries_list")["countries_list"].value_counts()
    if len(countries):
        share = countries.iloc[0] / countries.sum() * 100
        out.append(
            f"**Geography:** {countries.index[0]} is the largest source "
            f"({share:.0f}% of country tags); {len(countries)} countries are represented."
        )
        if countries.index[0] == "United States":
            out.append(
                f"**Regional diversification:** non-US countries account for "
                f"{100 - share:.0f}% of country tags."
            )

    genres = explode(df, "genres_list")["genres_list"].value_counts()
    if len(genres) >= 3:
        out.append("**Top genres:** " + ", ".join(genres.index[:3]) + ".")

    ratings = df["rating"].value_counts()
    if len(ratings):
        out.append(
            f"**Audience targeting:** {ratings.index[0]} is the most common rating "
            f"({ratings.iloc[0] / n * 100:.0f}% of titles)."
        )

    lag = df["release_lag"].dropna()
    if len(lag):
        out.append(
            f"**Release lag:** the median title arrives {lag.median():.0f} year(s) after release; "
            f"{(lag <= 2).mean() * 100:.0f}% are added within two years."
        )

    runtime = df["duration_min"].dropna()
    if len(runtime):
        out.append(f"**Movie runtime:** median {runtime.median():.0f} minutes.")
    seasons = df["seasons"].dropna()
    if len(seasons):
        out.append(f"**Series length:** {(seasons == 1).mean() * 100:.0f}% of TV shows have a single season.")
    return out