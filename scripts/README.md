# MoonLight Energy Solutions — Solar Dashboard

A Streamlit dashboard for cross-country solar irradiance analysis across
Benin, Togo, and Sierra Leone.

---

## Project Structure
```
solar-energy-analytics-1/
├── app/
│   ├── __init__.py
│   ├── main.py        # Main Streamlit application
│   └── utils.py       # Data loading and chart utilities
├── data/
│   ├── benin_clean.csv
│   ├── togo_clean.csv
│   └── sierra_leone_clean.csv
├── notebooks/
│   └── compare_countries.ipynb
└── scripts/
    ├── __init__.py
    └── README.md
```

---

## Requirements

Install all dependencies:
```bash
pip install streamlit plotly pandas scipy
```

---

## Running Locally

From the project root directory:
```bash
streamlit run app/main.py
```
Then open your browser at `http://localhost:8501`

---

## Dashboard Features

- **Sidebar checkboxes** — filter by country (Benin, Togo, Sierra Leone)
- **Average GHI Bar Chart** — ranks countries by solar potential
- **Boxplots** — GHI, DNI, DHI distribution per country side by side
- **Summary Statistics Table** — mean, median, std dev per metric per country
- **Kruskal-Wallis Test** — statistical significance of differences between countries

---

## Deploying to Streamlit Community Cloud

1. Push your code to GitHub (make sure `data/` is **not** in `.gitignore` 
   or the CSVs are accessible to the app)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Sign in with your GitHub account
4. Click **"New app"**
5. Fill in:
   - **Repository:** `your-github-username/solar-energy-analytics-1`
   - **Branch:** `main`
   - **Main file path:** `app/main.py`
6. Click **"Deploy"**
7. Wait ~2 minutes — your public URL will be ready

---

## Key Insights

| Rank | Country      | Avg GHI (W/m²) | Recommendation   |
|------|--------------|----------------|-----------------|
| 1    | Benin        | 477.40         | Strong Invest   |
| 2    | Togo         | 455.20         | Neutral         |
| 3    | Sierra Leone | 407.22         | Avoid           |

---

## Notes

- All analysis uses **daytime data only** (GHI > 0)
- Togo DNI values are affected by mechanical tracker failure
- Sierra Leone shows high variability due to Atlantic Monsoon patterns

---

*Built with Streamlit · MoonLight Energy Solutions*