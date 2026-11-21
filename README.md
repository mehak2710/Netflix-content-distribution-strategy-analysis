# 🎬 Netflix Content Distribution Strategy Analysis

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-E50914?logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458?logo=pandas&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)

An interactive **Streamlit** dashboard with a **Netflix-inspired** cinematic interface that analyses how Netflix distributes its content catalog across formats, countries, genres, maturity ratings and time.

> **Live demo:** _add your Streamlit Community Cloud link here_

<!-- Add a demo video or GIF here (see "Demo" below) -->
![Dashboard preview](assets/dashboard-preview.png)

---

## Table of Contents
- [Overview](#overview)
- [Business Questions](#business-questions)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Dataset](#dataset)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Getting Started](#getting-started)
- [Dashboard Walkthrough](#dashboard-walkthrough)
- [Highlights from the Data](#highlights-from-the-data)
- [Design Notes](#design-notes)
- [Deployment](#deployment)
- [Future Improvements](#future-improvements)
- [Acknowledgments](#acknowledgments)
- [Author](#author)

---

## Overview

Netflix's catalog is shaped by deliberate decisions about what to add, where to source it and who to target. This project turns the raw catalog (titles, countries, release years, date added, ratings, genres) into clear, explorable evidence of that strategy.

The analysis pipeline cleans the data, engineers analytical features, and serves the results through a filterable dashboard, so anyone can explore the findings without writing code.

## Business Questions

- Is Netflix leaning towards movies or TV shows, and has that changed over time?
- Which countries contribute the most content, and how diversified is the catalog beyond the US?
- How did content additions grow year over year, and is there seasonality in monthly additions?
- Which genres and maturity ratings dominate, and how does that differ by country?
- How long after release does a title reach Netflix?
- What is the typical movie runtime and number of seasons per show?

## Key Features

**Data cleaning and feature engineering**
- Handles missing values in director, cast and country columns
- Parses `date_added` into year and month features
- Splits multi-valued fields (genres, countries) so every value is counted correctly
- Standardises duration into minutes (movies) and seasons (TV shows)
- Fixes known data quirks, such as runtimes stored in the `rating` column
- Calculates release lag (year added minus release year)

**Analysis modules**
- Movies vs TV shows: content split and trend over time
- Growth analysis: titles added per year and per month
- Geographic distribution: top countries, world map and country trends
- Genre analysis: top genres and a genre-by-country heatmap
- Ratings analysis: audience targeting by maturity rating
- Release lag and duration distributions

**Interactive dashboard**
- Sidebar filters for content type, year added, country, genre and rating
- KPI cards: total titles, movie and TV share, number of countries, top country
- Netflix-style card rows: Top 10 Genres, Trending Countries, Recently Added
- Six tabs: Overview, Geography, Genres & Ratings, Duration & Lag, Title Search, Strategy Insights
- Search across title, cast, director and description
- Auto-generated strategy insights that update with the filters
- One-click download of the filtered dataset as CSV

**Netflix-inspired interface**
- Near-black background (`#141414`) with Netflix red (`#E50914`) accents
- Hero banner, ranked cards that zoom on hover, and a Bebas Neue wordmark header
- Dark-themed Plotly charts that blend into the page

## Tech Stack

| Layer | Tools |
|---|---|
| Language | Python 3.9+ |
| Data handling | Pandas, NumPy |
| Visualisation | Plotly (custom Netflix-themed styling) |
| Dashboard | Streamlit |
| Styling | Custom CSS injected via `st.markdown`, `.streamlit/config.toml` |
| Fonts | Google Fonts (Bebas Neue, Inter) |
| Version control and hosting | Git, GitHub, Streamlit Community Cloud |

## Dataset

[Netflix Movies and TV Shows](https://www.kaggle.com/datasets/shivamb/netflix-shows) by Shivam Bansal on Kaggle, collected from Flixable, a third-party Netflix search engine.

- About 8,800 titles added to Netflix up to 2021
- 12 columns: `show_id`, `type`, `title`, `director`, `cast`, `country`, `date_added`, `release_year`, `rating`, `duration`, `listed_in`, `description`
- Check the license and terms on the Kaggle page before redistributing the data

## Project Structure

```
netflix-content-analysis/
├── app.py                      # Streamlit dashboard (UI, filters, charts, tabs)
├── requirements.txt            # Python dependencies
├── README.md
├── .gitignore
├── .streamlit/
│   └── config.toml             # Dark theme and Netflix red accent
├── assets/
│   └── dashboard-preview.png   # Screenshot used in this README
├── data/
│   └── netflix_titles.csv      # Kaggle dataset
└── utils/
    ├── __init__.py
    ├── cleaning.py             # Loading, cleaning, feature engineering
    ├── insights.py             # Auto-generated strategy insights
    └── theme.py                # Netflix CSS, Plotly styling, card rows
```

## How It Works

```
netflix_titles.csv → cleaning.py → app.py → filters → KPIs, cards, charts, search, download
                                       └→ insights.py (takeaways)   └→ theme.py (styling)
```

1. `cleaning.py` loads the CSV, fills missing values, parses dates, and creates analysis-ready columns.
2. `app.py` applies the user's sidebar filters to the cleaned data.
3. `insights.py` and the chart code read the filtered data, so every number on screen reflects the current selection.
4. `theme.py` provides the visual identity shared by the cards and charts.

## Getting Started

### Prerequisites
- Python 3.9 or newer
- pip

### Installation

```bash
# 1. Clone the repository
git clone https://github.com/mehak2710/netflix-content-distribution-strategy-analysis.git
cd netflix-content-distribution-strategy-analysis

# 2. (Recommended) create a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# Mac/Linux
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the app
streamlit run app.py
```

The app opens at `http://localhost:8501`. Run the command from the project root so that the `utils` package and the `data/` folder are found. You can also upload a different `netflix_titles.csv` from the sidebar.

## Dashboard Walkthrough

| Tab | What you will find |
|---|---|
| Overview | Movies vs TV split, titles added per year, TV share trend, monthly seasonality |
| Geography | Top 15 countries, world map, top-5 country trends over time |
| Genres & Ratings | Top genres, maturity ratings, genre-by-country heatmap |
| Duration & Lag | Movie runtime, seasons per show, release lag distribution and trend |
| Title Search | Search by title, cast, director or description |
| Strategy Insights | Plain-language takeaways generated from the current filters |

## Highlights from the Data

- About **70%** of the catalog is movies and **30%** TV shows
- The **United States** is the largest source with about 3,690 titles, followed by **India** (about 1,046) and the **United Kingdom** (about 806)
- **International Movies**, **Dramas** and **Comedies** are the three most common genres
- Content from over 120 countries is represented

Use the sidebar filters and the Strategy Insights tab to explore more, such as the TV share of additions by year or how release lag changed over time.

## Design Notes

The interface is **Netflix-inspired**. It uses a text wordmark and a similar colour palette and layout. Netflix's logo, fonts and artwork are trademarks of Netflix, Inc. and are not used. This project is for educational and portfolio purposes and is not affiliated with or endorsed by Netflix.


## Future Improvements

- Enrich the data with IMDb or Rotten Tomatoes ratings
- Add actor and director network analysis
- Add title similarity search using text embeddings of descriptions
- Add a recommendation view based on genre and country
- Add automated tests for the cleaning functions
