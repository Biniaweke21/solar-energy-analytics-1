# app/main.py
import streamlit as st
import sys
import os

# ── Path setup so app can find utils.py ──────────────────────────────────────
sys.path.append(os.path.dirname(__file__))
from utils import load_data, make_boxplot, make_ghi_ranking, make_summary_table, run_kruskal

# ── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title = "MoonLight Energy Solutions",
    page_icon  = "☀️",
    layout     = "wide"
)

# ── Header ────────────────────────────────────────────────────────────────────
st.title("☀️ West African Solar Investment Dashboard")
st.markdown("**MoonLight Energy Solutions** — Cross-Country Solar Irradiance Analysis")
st.markdown("---")

# ── Load Data ─────────────────────────────────────────────────────────────────
with st.spinner("Loading data..."):
    df_all = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.title("🌍 Filter Countries")
st.sidebar.markdown("Select countries to include in the analysis:")

show_benin        = st.sidebar.checkbox("Benin",        value=True)
show_togo         = st.sidebar.checkbox("Togo",         value=True)
show_sierra_leone = st.sidebar.checkbox("Sierra Leone", value=True)

selected_countries = []
if show_benin:        selected_countries.append("Benin")
if show_togo:         selected_countries.append("Togo")
if show_sierra_leone: selected_countries.append("Sierra Leone")

# ── Guard: at least one country must be selected ──────────────────────────────
if not selected_countries:
    st.warning("⚠️ Please select at least one country from the sidebar.")
    st.stop()

# ── Filter dataframe ──────────────────────────────────────────────────────────
df = df_all[df_all["Country"].isin(selected_countries)]

st.sidebar.markdown("---")
st.sidebar.markdown(f"**Rows loaded:** {len(df):,}")
st.sidebar.markdown(f"**Countries:** {', '.join(selected_countries)}")

# ── Section 1: GHI Ranking Bar Chart ─────────────────────────────────────────
st.subheader("📊 Average GHI Ranking")
st.markdown("Countries ranked by average Global Horizontal Irradiance (daytime only).")
st.plotly_chart(make_ghi_ranking(df), use_container_width=True)

st.markdown("---")

# ── Section 2: Boxplots ───────────────────────────────────────────────────────
st.subheader("📦 Irradiance Distribution (Boxplots)")
st.markdown("Compare the spread, median, and variability of GHI, DNI, and DHI per country.")

col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(make_boxplot(df, "GHI"), use_container_width=True)
with col2:
    st.plotly_chart(make_boxplot(df, "DNI"), use_container_width=True)
with col3:
    st.plotly_chart(make_boxplot(df, "DHI"), use_container_width=True)

st.markdown("---")

# ── Section 3: Summary Statistics Table ──────────────────────────────────────
st.subheader("📋 Summary Statistics Table")
st.markdown("Mean, Median, and Standard Deviation for each metric per country.")

summary_df = make_summary_table(df)
st.dataframe(
    summary_df.style.format({"Mean": "{:.2f}", "Median": "{:.2f}", "Std Dev": "{:.2f}"}),
    use_container_width = True,
    hide_index          = True
)

st.markdown("---")

# ── Section 4: Kruskal-Wallis Results ────────────────────────────────────────
st.subheader("🧪 Kruskal-Wallis Statistical Test")
st.markdown("""
Tests whether differences in GHI, DNI, and DHI across countries are statistically significant.
- **H₀:** All countries share the same distribution
- **H₁:** At least one country differs significantly (α = 0.05)
""")

if len(selected_countries) < 2:
    st.info("ℹ️ Select at least 2 countries to run the statistical test.")
else:
    kw_df = run_kruskal(df)
    st.dataframe(kw_df, use_container_width=True, hide_index=True)

st.markdown("---")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown(
    "<div style='text-align:center; color:gray; font-size:13px;'>"
    "MoonLight Energy Solutions · Solar Investment Analysis · Built with Streamlit"
    "</div>",
    unsafe_allow_html=True
)