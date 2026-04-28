from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st

from utils import COUNTRIES, load_all_countries


st.set_page_config(page_title="Climate Insights Dashboard", layout="wide")
sns.set_theme(style="whitegrid")

st.title("Climate Insights Dashboard")
st.caption("Interactive cross-country climate exploration (NASA POWER datasets)")

data_dir = (Path(__file__).resolve().parent.parent / "data").resolve()

if not data_dir.exists():
    st.error("Data folder not found. Expected folder: data/")
    st.stop()

try:
    df = load_all_countries(data_dir, COUNTRIES)
except Exception as exc:
    st.error(f"Failed to load data: {exc}")
    st.stop()

if df.empty or "Date" not in df.columns:
    st.error("No usable data loaded.")
    st.stop()

available_years = sorted(df["Year"].dropna().unique().tolist())
if not available_years:
    st.error("No valid years detected in dataset.")
    st.stop()

st.sidebar.header("Filters")
selected_countries = st.sidebar.multiselect(
    "Select countries",
    options=sorted(df["Country"].dropna().unique().tolist()),
    default=sorted(df["Country"].dropna().unique().tolist()),
)

year_min, year_max = int(min(available_years)), int(max(available_years))
selected_year_range = st.sidebar.slider(
    "Year range",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max),
)

variable_options = [col for col in ["T2M", "PRECTOTCORR", "RH2M", "WS2M", "T2M_MAX", "T2M_MIN"] if col in df.columns]
selected_variable = st.sidebar.selectbox(
    "Variable",
    options=variable_options,
    index=0 if variable_options else None,
)

if not selected_countries:
    st.warning("Select at least one country to display charts.")
    st.stop()

filtered = df[
    (df["Country"].isin(selected_countries))
    & (df["Year"] >= selected_year_range[0])
    & (df["Year"] <= selected_year_range[1])
].copy()

if filtered.empty:
    st.warning("No data available for the current filter selection.")
    st.stop()

left, right = st.columns(2)
with left:
    st.metric("Rows", f"{len(filtered):,}")
with right:
    st.metric("Countries", f"{filtered['Country'].nunique()}")

st.subheader("Monthly Trend by Country")
monthly = (
    filtered.groupby(["Country", pd.Grouper(key="Date", freq="ME")])[selected_variable]
    .mean()
    .reset_index()
)

fig1, ax1 = plt.subplots(figsize=(12, 5))
sns.lineplot(data=monthly, x="Date", y=selected_variable, hue="Country", ax=ax1)
ax1.set_title(f"Monthly Average {selected_variable} by Country")
ax1.set_xlabel("Date")
ax1.set_ylabel(selected_variable)
st.pyplot(fig1)

st.subheader("Precipitation Distribution by Country")
if "PRECTOTCORR" in filtered.columns:
    fig2, ax2 = plt.subplots(figsize=(12, 5))
    sns.boxplot(data=filtered, x="Country", y="PRECTOTCORR", ax=ax2)
    ax2.set_title("Daily PRECTOTCORR Distribution")
    ax2.set_xlabel("Country")
    ax2.set_ylabel("PRECTOTCORR (mm/day)")
    st.pyplot(fig2)
else:
    st.info("PRECTOTCORR column not available in the selected data.")

st.subheader("Filtered Data Preview")
st.dataframe(
    filtered[["Country", "Date", "YEAR", "DOY", selected_variable, "PRECTOTCORR"]]
    .sort_values(["Country", "Date"])
    .tail(200),
    use_container_width=True,
)
