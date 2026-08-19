import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Analytics", page_icon="📊", layout="wide")


@st.cache_data
def load_data(seed: int = 42) -> pd.DataFrame:
    """Generate a synthetic sales dataset.

    Replace the body with a real source when ready, e.g.:
        return pd.read_csv("your_data.csv", parse_dates=["date"])
    Expected columns: date, region, category, channel, units, revenue, profit.
    """
    rng = np.random.default_rng(seed)
    n = 5000
    dates = pd.date_range("2023-01-01", "2024-12-31", freq="D")

    regions = ["North", "South", "East", "West"]
    categories = ["Electronics", "Apparel", "Home", "Sports", "Books"]
    channels = ["Online", "Retail", "Wholesale"]

    df = pd.DataFrame({
        "date": rng.choice(dates, n),
        "region": rng.choice(regions, n, p=[0.3, 0.25, 0.25, 0.2]),
        "category": rng.choice(categories, n),
        "channel": rng.choice(channels, n, p=[0.5, 0.35, 0.15]),
        "units": rng.integers(1, 25, n),
    })
    base_price = {"Electronics": 320, "Apparel": 55, "Home": 90,
                  "Sports": 75, "Books": 20}
    df["unit_price"] = df["category"].map(base_price) * rng.uniform(0.8, 1.3, n)
    df["revenue"] = (df["units"] * df["unit_price"]).round(2)
    df["cost"] = (df["revenue"] * rng.uniform(0.55, 0.8, n)).round(2)
    df["profit"] = (df["revenue"] - df["cost"]).round(2)
    return df.sort_values("date").reset_index(drop=True)


df = load_data()

st.sidebar.header("Filters")

date_min, date_max = df["date"].min(), df["date"].max()
date_range = st.sidebar.date_input(
    "Date range", value=(date_min, date_max),
    min_value=date_min, max_value=date_max,
)

regions = st.sidebar.multiselect(
    "Region", sorted(df["region"].unique()), default=sorted(df["region"].unique())
)
categories = st.sidebar.multiselect(
    "Category", sorted(df["category"].unique()), default=sorted(df["category"].unique())
)
channels = st.sidebar.multiselect(
    "Channel", sorted(df["channel"].unique()), default=sorted(df["channel"].unique())
)

mask = (
    df["region"].isin(regions)
    & df["category"].isin(categories)
    & df["channel"].isin(channels)
)
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
    mask &= df["date"].between(start, end)

fdf = df[mask]

st.title("📊 Sales Analytics Dashboard")
st.caption("Interactive demo — filter in the sidebar. Built with Streamlit + Plotly.")

if fdf.empty:
    st.warning("No data matches the current filters.")
    st.stop()

c1, c2, c3, c4 = st.columns(4)
c1.metric("Revenue", f"${fdf['revenue'].sum():,.0f}")
c2.metric("Profit", f"${fdf['profit'].sum():,.0f}")
c3.metric("Units Sold", f"{fdf['units'].sum():,}")
margin = fdf["profit"].sum() / fdf["revenue"].sum() * 100
c4.metric("Profit Margin", f"{margin:.1f}%")

st.divider()

left, right = st.columns(2)

with left:
    st.subheader("Revenue Over Time")
    ts = fdf.set_index("date").resample("W")["revenue"].sum().reset_index()
    fig = px.line(ts, x="date", y="revenue", markers=False)
    fig.update_layout(margin=dict(t=10, b=0, l=0, r=0), height=320)
    st.plotly_chart(fig, width='stretch')

with right:
    st.subheader("Revenue by Category")
    by_cat = fdf.groupby("category")["revenue"].sum().reset_index()
    fig = px.bar(by_cat.sort_values("revenue"), x="revenue", y="category",
                 orientation="h", color="revenue", color_continuous_scale="Blues")
    fig.update_layout(margin=dict(t=10, b=0, l=0, r=0), height=320,
                      coloraxis_showscale=False)
    st.plotly_chart(fig, width='stretch')

left2, right2 = st.columns(2)

with left2:
    st.subheader("Channel Mix")
    by_ch = fdf.groupby("channel")["revenue"].sum().reset_index()
    fig = px.pie(by_ch, names="channel", values="revenue", hole=0.5)
    fig.update_layout(margin=dict(t=10, b=0, l=0, r=0), height=320)
    st.plotly_chart(fig, width='stretch')

with right2:
    st.subheader("Region × Category Revenue")
    pivot = fdf.pivot_table(index="region", columns="category",
                            values="revenue", aggfunc="sum", fill_value=0)
    fig = px.imshow(pivot, aspect="auto", color_continuous_scale="Blues",
                    labels=dict(color="Revenue"))
    fig.update_layout(margin=dict(t=10, b=0, l=0, r=0), height=320)
    st.plotly_chart(fig, width='stretch')

st.divider()
st.subheader("Filtered Records")
st.dataframe(fdf, width='stretch', height=280)

st.download_button(
    "⬇️ Download filtered data (CSV)",
    fdf.to_csv(index=False).encode("utf-8"),
    file_name="filtered_sales.csv",
    mime="text/csv",
)
