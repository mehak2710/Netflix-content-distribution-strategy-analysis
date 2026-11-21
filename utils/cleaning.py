"""Data loading, cleaning and feature engineering for the Netflix catalog."""
from __future__ import annotations

import pandas as pd

MONTH_ORDER = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def _split(value: str) -> list[str]:
    """Split a comma-separated string into a clean list."""
    items = [v.strip() for v in str(value).split(",") if v.strip()]
    return items or ["Unknown"]


def clean(raw: pd.DataFrame) -> pd.DataFrame:
    """Return a cleaned copy of the raw netflix_titles dataframe."""
    df = raw.copy()
    df.columns = [c.strip().lower() for c in df.columns]

    # Text columns
    for col in ["director", "cast", "country", "description", "listed_in"]:
        if col not in df.columns:
            df[col] = "Unknown"
        df[col] = df[col].fillna("Unknown").astype(str).str.strip()
    df["type"] = df["type"].astype(str).str.strip()
    df["title"] = df["title"].astype(str).str.strip()

    # A few rows in the Kaggle file have the runtime stored in `rating`
    bad_rating = df["rating"].astype(str).str.contains("min", na=False)
    df.loc[bad_rating & df["duration"].isna(), "duration"] = df.loc[bad_rating, "rating"]
    df.loc[bad_rating, "rating"] = "Not Rated"
    df["rating"] = df["rating"].fillna("Not Rated").astype(str).str.strip()
    df["rating"] = df["rating"].replace({"NR": "Not Rated", "UR": "Not Rated"})

    # Dates
    df["date_added"] = pd.to_datetime(
        df["date_added"].astype(str).str.strip(), format="mixed", errors="coerce"
    )
    df["year_added"] = df["date_added"].dt.year
    df["month_added"] = pd.Categorical(
        df["date_added"].dt.month_name(), categories=MONTH_ORDER, ordered=True
    )
    df["release_year"] = pd.to_numeric(df["release_year"], errors="coerce")
    df["release_lag"] = (df["year_added"] - df["release_year"]).clip(lower=0)

    # Duration: minutes for movies, seasons for TV shows
    num = df["duration"].astype(str).str.extract(r"(\d+)")[0].astype(float)
    df["duration_min"] = num.where(df["type"] == "Movie")
    df["seasons"] = num.where(df["type"] == "TV Show")

    # Multi-valued fields
    df["countries_list"] = df["country"].apply(_split)
    df["genres_list"] = df["listed_in"].apply(_split)
    df["primary_country"] = df["countries_list"].str[0]
    return df


def explode(df: pd.DataFrame, col: str, drop_unknown: bool = True) -> pd.DataFrame:
    """One row per value of a list column (e.g. genres_list, countries_list)."""
    out = df.explode(col)
    if drop_unknown:
        out = out[out[col] != "Unknown"]
    return out