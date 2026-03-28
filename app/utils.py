# app/utils.py
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import kruskal

# ── Constants ─────────────────────────────────────────────────────────────────
COUNTRY_COLORS = {
    "Benin"       : "#F4A623",
    "Togo"        : "#2ECC71",
    "Sierra Leone": "#3498DB"
}

METRICS = ["GHI", "DNI", "DHI"]

# ── Data Loading ──────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    benin        = pd.read_csv("data/benin_clean.csv")
    togo         = pd.read_csv("data/togo_clean.csv")
    sierra_leone = pd.read_csv("data/SierraLeone_clean.csv")

    benin["Country"]        = "Benin"
    togo["Country"]         = "Togo"
    sierra_leone["Country"] = "Sierra Leone"

    df = pd.concat([benin, togo, sierra_leone], ignore_index=True)
    df = df[df["GHI"] > 0].reset_index(drop=True)
    return df

# ── Boxplot ───────────────────────────────────────────────────────────────────
def make_boxplot(df, metric):
    fig = px.box(
        df,
        x              = "Country",
        y              = metric,
        color          = "Country",
        color_discrete_map = COUNTRY_COLORS,
        title          = f"{metric} Distribution by Country",
        labels         = {metric: "W/m²"},
        category_orders= {"Country": ["Benin", "Togo", "Sierra Leone"]}
    )
    fig.update_layout(
        plot_bgcolor  = "white",
        showlegend    = False,
        title_font    = dict(size=16, family="Arial"),
        yaxis         = dict(gridcolor="#eeeeee"),
        xaxis_title   = ""
    )
    return fig

# ── Average GHI Bar Chart ─────────────────────────────────────────────────────
def make_ghi_ranking(df):
    avg_ghi = (df.groupby("Country")["GHI"]
                 .mean()
                 .reindex(["Benin", "Togo", "Sierra Leone"])
                 .reset_index())
    avg_ghi.columns = ["Country", "Average GHI"]
    avg_ghi["Average GHI"] = avg_ghi["Average GHI"].round(2)

    fig = px.bar(
        avg_ghi,
        x                  = "Country",
        y                  = "Average GHI",
        color              = "Country",
        color_discrete_map = COUNTRY_COLORS,
        title              = "Average GHI Ranking by Country",
        labels             = {"Average GHI": "W/m²"},
        text               = "Average GHI"
    )
    fig.update_traces(texttemplate="%{text} W/m²", textposition="outside")
    fig.update_layout(
        plot_bgcolor = "white",
        showlegend   = False,
        title_font   = dict(size=16, family="Arial"),
        yaxis        = dict(gridcolor="#eeeeee"),
        xaxis_title  = ""
    )
    return fig

# ── Summary Statistics Table ──────────────────────────────────────────────────
def make_summary_table(df):
    rows = []
    for country in ["Benin", "Togo", "Sierra Leone"]:
        df_c = df[df["Country"] == country]
        for metric in METRICS:
            rows.append({
                "Country" : country,
                "Metric"  : metric,
                "Mean"    : round(df_c[metric].mean(), 2),
                "Median"  : round(df_c[metric].median(), 2),
                "Std Dev" : round(df_c[metric].std(), 2),
            })
    return pd.DataFrame(rows)

# ── Kruskal-Wallis Test ───────────────────────────────────────────────────────
def run_kruskal(df):
    results = []
    for metric in METRICS:
        groups = [
            df[df["Country"] == c][metric].dropna()
            for c in ["Benin", "Togo", "Sierra Leone"]
        ]
        h_stat, p_value = kruskal(*groups)
        results.append({
            "Metric"      : metric,
            "H-Statistic" : round(h_stat, 2),
            "p-value"     : f"{p_value:.2e}",
            "Significant" : "✅ Yes" if p_value < 0.05 else "❌ No"
        })
    return pd.DataFrame(results)