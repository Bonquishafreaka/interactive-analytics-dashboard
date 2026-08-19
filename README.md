# Sales Analytics Dashboard

An interactive analytics dashboard built with Streamlit and Plotly. Filter by date, region, category, and channel, and see KPIs and charts update in real time.

> **Note:** The app ships with a synthetic dataset generated at runtime, so it runs immediately with no data setup. See [Using your own data](#using-your-own-data) to plug in a real source.

## Features

- Sidebar filters: date range, region, category, channel
- KPI cards: revenue, profit, units sold, profit margin
- Four chart types: time series, horizontal bar, donut, heatmap
- Filterable data table with CSV export

## Quickstart

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt

streamlit run dashboard.py
```

Then open the URL Streamlit prints (default: http://localhost:8501).

> On Windows, if `streamlit` isn't recognized, run it as a module:
> ```bash
> python -m streamlit run dashboard.py
> ```

## Using your own data

All data comes from the `load_data()` function in `dashboard.py`. Replace its body with a real source, for example:

```python
@st.cache_data
def load_data():
    return pd.read_csv("your_data.csv", parse_dates=["date"])
```

The rest of the app expects these columns: `date`, `region`, `category`, `channel`, `units`, `revenue`, `profit`.

## Deploy

- **Streamlit Community Cloud** — push to GitHub, connect at share.streamlit.io. Auto-installs from `requirements.txt`.
- **Hugging Face Spaces** — create a Space with the Streamlit SDK.

## Tech stack

Python · Streamlit · Plotly · pandas · NumPy
