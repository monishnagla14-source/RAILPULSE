from pathlib import Path
from datetime import date
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "train_delays.csv"

# Dark theme auto-setup: agar .streamlit/config.toml nahi hai to ye khud bana deta hai.
# (Bante hi theme apply nahi hota to ek baar Ctrl+C karke app dobara chala dena.)
try:
    _cfg = Path.cwd() / ".streamlit" / "config.toml"
    if not _cfg.exists():
        _cfg.parent.mkdir(exist_ok=True)
        _cfg.write_text('[theme]\nbase = "dark"\n', encoding="utf-8")
except OSError:
    pass

st.set_page_config(page_title="RailPulse | Train Delay Analytics", page_icon="🚆", layout="wide", initial_sidebar_state="expanded")

# ---------- Styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Space+Grotesk:wght@500;600;700&display=swap');
:root { --ink:#eaf0fa; --muted:#9baac1; --panel:#111d30; --line:#263750; --accent:#f5a524; }
.stApp { background: radial-gradient(ellipse at 10% 0%, #1b3150 0%, #0a1220 42%, #080e18 100%); color:var(--ink); font-family:'DM Sans',sans-serif; }
[data-testid="stHeader"] { background:rgba(8,14,24,.72); }
[data-testid="stSidebar"] { background:#0d1727; border-right:1px solid #24334a; }
[data-testid="stSidebar"] * { color:#eaf0fa; }
.block-container { padding-top:1.7rem; max-width:1440px; }
h1,h2,h3 { font-family:'Space Grotesk',sans-serif !important; color:#f2f6ff !important; }
.eyebrow { text-transform:uppercase; letter-spacing:.18em; color:#f5a524; font-size:.73rem; font-weight:700; }
.hero { border:1px solid #2b3c56; border-radius:24px; padding:28px 32px; background:linear-gradient(120deg,rgba(24,43,69,.96),rgba(14,26,43,.92)); position:relative; overflow:hidden; }
.hero:after { content:'🚆'; position:absolute; right:35px; top:12px; font-size:78px; opacity:.16; }
.hero-title { font-family:'Space Grotesk',sans-serif; font-size:clamp(2rem,4vw,3.25rem); font-weight:700; letter-spacing:-.04em; line-height:1.08; margin:.35rem 0 .7rem; }
.hero-sub { color:#b6c4d8; max-width:720px; font-size:1rem; line-height:1.65; }
.pill { display:inline-block; border:1px solid #3a4e6a; background:#1a2b43; color:#c9d7e9; padding:5px 10px; border-radius:999px; font-size:.75rem; margin-right:6px; }

/* Fix for overlapping Metric cards container in Streamlit dark mode */
div[data-testid="stMetric"] { background:#111d30 !important; border:1px solid #293b55 !important; padding:14px 16px !important; border-radius:15px !important; position: relative !important; z-index: 2 !important; }
div[data-testid="stMetricLabel"], div[data-testid="stMetricLabel"] * { color:#c3d0e3 !important; }
div[data-testid="stMetricValue"], div[data-testid="stMetricValue"] * { color:#f4f7ff !important; }

/* ---------- Sidebar inputs: dark box + white text (date range, Train, Route) ---------- */
[data-testid="stSidebar"] { color-scheme: dark; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] label p { color:#eaf0fa !important; }

/* box + uske andar ka har element ek hi dark colour (koi white patch nahi bachega) */
[data-testid="stSidebar"] [data-testid="stDateInput"] div[data-baseweb],
[data-testid="stSidebar"] [data-testid="stDateInput"] div[data-baseweb] *,
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb],
[data-testid="stSidebar"] [data-testid="stSelectbox"] div[data-baseweb] *,
[data-testid="stSidebar"] div[data-baseweb="select"] > div,
[data-testid="stSidebar"] div[data-baseweb="input"],
[data-testid="stSidebar"] div[data-baseweb="base-input"],
[data-testid="stSidebar"] div[data-baseweb="input"] input,
[data-testid="stSidebar"] div[data-baseweb="select"] input {
    background:#0a1424 !important;
    background-color:#0a1424 !important;
    color:#ffffff !important;
    -webkit-text-fill-color:#ffffff !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div,
[data-testid="stSidebar"] div[data-baseweb="input"] {
    border:1px solid #2b3c56 !important;
    border-radius:10px !important;
}
[data-testid="stSidebar"] div[data-baseweb="select"] > div:hover,
[data-testid="stSidebar"] div[data-baseweb="input"]:hover { border-color:#3b506d !important; }
[data-testid="stSidebar"] div[data-baseweb="select"] > div:focus-within,
[data-testid="stSidebar"] div[data-baseweb="input"]:focus-within { border-color:#f5a524 !important; }

[data-testid="stSidebar"] input::placeholder {
    color:rgba(255,255,255,.55) !important;
    -webkit-text-fill-color:rgba(255,255,255,.55) !important;
}
/* dropdown arrow + calendar icon */
[data-testid="stSidebar"] div[data-baseweb="select"] svg,
[data-testid="stSidebar"] div[data-baseweb="input"] svg { fill:#ffffff !important; color:#ffffff !important; }

/* Popups (open ho kar sidebar ke bahar render hote hain, isliye sidebar selector nahi lagaya) */
div[data-baseweb="popover"] > div,
div[data-baseweb="popover"] ul,
div[data-baseweb="popover"] li { background-color:#0f1b2e !important; }
div[data-baseweb="popover"] li,
div[data-baseweb="popover"] li * { color:#ffffff !important; }
div[data-baseweb="popover"] li:hover,
div[data-baseweb="popover"] li[aria-selected="true"] { background-color:#1d2f4a !important; }

div[data-baseweb="calendar"] { background-color:#0f1b2e !important; color:#ffffff !important; }
div[data-baseweb="calendar"] * { color:#ffffff !important; }
div[data-baseweb="calendar"] [aria-disabled="true"],
div[data-baseweb="calendar"] [aria-disabled="true"] * { color:rgba(255,255,255,.3) !important; }

.section-head { font-family:'Space Grotesk',sans-serif; font-size:1.25rem; font-weight:600; color:#edf3ff; margin:1.1rem 0 .2rem; }
.section-note { color:#9baac1; font-size:.86rem; margin-bottom:.8rem; }
.stButton>button { border-radius:10px; border:1px solid #3b506d; font-weight:600; }
.stButton>button[kind="primary"] { background:#f5a524; color:#101827; border:none; }
[data-testid="stDataFrame"] { border:1px solid #293b55; border-radius:12px; overflow:hidden; }
hr { border-color:#263750; }
.small-muted { color:#91a3bc; font-size:.78rem; }
</style>
""", unsafe_allow_html=True)

# ---------- Data ----------
def load_data() -> pd.DataFrame:
    if not DATA_FILE.exists():
        st.error("Dataset file not found. Make sure data/train_delays.csv is inside the project folder.")
        st.stop()
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    required = {"date", "train_no", "train_name", "origin", "destination", "scheduled_minutes", "actual_minutes", "distance_km"}
    missing = required - set(df.columns)
    if missing:
        st.error(f"Dataset is missing required columns: {', '.join(sorted(missing))}")
        st.stop()
    df["delay_minutes"] = (df["actual_minutes"] - df["scheduled_minutes"]).clip(lower=0)
    df["on_time"] = df["delay_minutes"] <= 10
    df["month"] = df["date"].dt.strftime("%b %Y")
    df["route"] = df["origin"] + " → " + df["destination"]
    return df

raw_df = load_data()

# ---------- Sidebar filters ----------
st.sidebar.markdown("<div class='eyebrow'>RAILPULSE</div><h2 style='margin-top:4px'>Control panel</h2>", unsafe_allow_html=True)
st.sidebar.caption("Explore the included historical-style sample dataset.")

min_date = raw_df["date"].min().date()
max_date = raw_df["date"].max().date()
selected_dates = st.sidebar.date_input("Travel date range", value=(min_date, max_date), min_value=min_date, max_value=max_date)

# Safe unpacking of date input.
# Jab user range me sirf start date click karta hai, Streamlit 1-item tuple (date,) deta hai;
# khali ho to () deta hai. Teeno cases yahan handle hote hain.
def resolve_date_range(selected, fallback_start, fallback_end):
    picked = list(selected) if isinstance(selected, (tuple, list)) else [selected]
    picked = [d for d in picked if d is not None]
    if len(picked) >= 2:
        start, end = picked[0], picked[1]
    elif len(picked) == 1:
        start = end = picked[0]
    else:
        start, end = fallback_start, fallback_end
    if start > end:
        start, end = end, start
    return start, end

start_date, end_date = resolve_date_range(selected_dates, min_date, max_date)

# Date-filtered base for dependent dropdowns
date_filtered = raw_df[(raw_df["date"].dt.date >= start_date) & (raw_df["date"].dt.date <= end_date)]

# 1. Train Dropdown (Defined first)
train_options = ["All trains"] + sorted(date_filtered["train_name"].unique().tolist())
selected_train = st.sidebar.selectbox("Train", train_options)

# 2. Route Dropdown (Dependent on selected_train)
if selected_train != "All trains":
    route_options = ["All routes"] + sorted(date_filtered[date_filtered["train_name"] == selected_train]["route"].unique().tolist())
else:
    route_options = ["All routes"] + sorted(date_filtered["route"].unique().tolist())
selected_route = st.sidebar.selectbox("Route", route_options)

max_delay = st.sidebar.slider("Maximum delay to include (minutes)", min_value=0, max_value=max(60, int(raw_df["delay_minutes"].max())), value=max(60, int(raw_df["delay_minutes"].max())), step=5)

# Final filtering
filtered = date_filtered.copy()
if selected_train != "All trains":
    filtered = filtered[filtered["train_name"] == selected_train]
if selected_route != "All routes":
    filtered = filtered[filtered["route"] == selected_route]
filtered = filtered[filtered["delay_minutes"] <= max_delay]

# ---------- Header ----------
st.markdown("""
<div class="hero">
  <div class="eyebrow">RAILWAY DATA • EXPLORATION • INSIGHTS</div>
  <div class="hero-title">Every minute tells<br> a railway story.</div>
  <div class="hero-sub">RailPulse turns train timing records into clear, useful insights. Compare punctuality, explore routes, and understand delay patterns — all from one simple dashboard.</div>
  <div style="margin-top:18px"><span class="pill">📊 Data analytics</span><span class="pill">🧭 Route comparison</span><span class="pill">🧪 Student project</span></div>
</div>
""", unsafe_allow_html=True)
st.markdown("<div class='small-muted' style='margin-top:12px'>⚠️ Demo disclaimer: this project uses an included sample CSV dataset. It does not show live train status or official Indian Railways information.</div>", unsafe_allow_html=True)

if filtered.empty:
    st.warning("No records match these filters. Try widening the date range or increasing the maximum delay.")
    st.stop()

# ---------- KPI calculations (Pandas + NumPy) ----------
record_count = len(filtered)
avg_delay = float(np.mean(filtered["delay_minutes"].to_numpy()))
median_delay = float(np.median(filtered["delay_minutes"].to_numpy()))
on_time_pct = float(np.mean(filtered["on_time"].to_numpy()) * 100)
route_count = filtered["route"].nunique()

st.markdown("<div class='section-head'>Network snapshot</div><div class='section-note'>Summary of the records matching your filters.</div>", unsafe_allow_html=True)
k1, k2, k3, k4 = st.columns(4)
with k1: st.metric("Records analyzed", f"{record_count:,}", help="Number of sample train-day records after filters")
with k2: st.metric("Average delay", f"{avg_delay:.1f} min", help="Mean delay, calculated with NumPy")
with k3: st.metric("On-time rate", f"{on_time_pct:.1f}%", help="In this demo, on-time means delay of 10 minutes or less")
with k4: st.metric("Routes covered", f"{route_count}", help="Unique origin-destination pairs in the filtered data")

# ---------- Charts ----------
st.markdown("<div class='section-head'>Delay patterns</div><div class='section-note'>Charts update when you change the filters.</div>", unsafe_allow_html=True)
left, right = st.columns([1.25, 1])
plt.rcParams.update({"text.color":"#dce6f5", "axes.labelcolor":"#b8c7dc", "xtick.color":"#b8c7dc", "ytick.color":"#b8c7dc", "axes.edgecolor":"#354761", "font.size":9})
with left:
    by_train = filtered.groupby("train_name", as_index=False)["delay_minutes"].mean().sort_values("delay_minutes", ascending=False).head(8)
    fig, ax = plt.subplots(figsize=(8, 4.1), facecolor="#111d30")
    ax.set_facecolor("#111d30")
    bars = ax.barh(by_train["train_name"], by_train["delay_minutes"], color="#f5a524")
    ax.invert_yaxis(); ax.set_xlabel("Average delay (minutes)"); ax.set_title("Average delay by train", color="#f0f5ff", loc="left", pad=12, fontweight="bold")
    ax.grid(axis="x", color="#2b3d56", alpha=.7); ax.set_axisbelow(True)
    for spine in ax.spines.values(): spine.set_visible(False)
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
with right:
    on_time_count = int(filtered["on_time"].sum())
    delayed_count = int(record_count - on_time_count)
    fig, ax = plt.subplots(figsize=(6, 4.1), facecolor="#111d30")
    ax.set_facecolor("#111d30")
    wedges, texts, autotexts = ax.pie([on_time_count, delayed_count], labels=["On time ≤10m", "Over 10m"], autopct="%1.0f%%", startangle=90, colors=["#39c6a5", "#f5a524"], textprops={"color":"#e6eefb"}, wedgeprops={"width":.42,"edgecolor":"#111d30","linewidth":3})
    for t in autotexts: t.set_color("#0a1220"); t.set_fontweight("bold")
    ax.set_title("Punctuality split", color="#f0f5ff", loc="left", pad=12, fontweight="bold")
    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

# Monthly trend
monthly = filtered.groupby(filtered["date"].dt.to_period("M"))["delay_minutes"].mean().reset_index()
monthly["month"] = monthly["date"].astype(str)
fig, ax = plt.subplots(figsize=(11, 3.5), facecolor="#111d30")
ax.set_facecolor("#111d30")
ax.plot(monthly["month"], monthly["delay_minutes"], color="#62a8ff", marker="o", linewidth=2.5, markersize=6)
ax.fill_between(range(len(monthly)), monthly["delay_minutes"].to_numpy(), alpha=.13, color="#62a8ff")
ax.set_title("Average delay over time", color="#f0f5ff", loc="left", pad=12, fontweight="bold")
ax.set_ylabel("Minutes"); ax.grid(axis="y", color="#2b3d56", alpha=.7); ax.set_axisbelow(True)
for spine in ax.spines.values(): spine.set_visible(False)
ax.tick_params(axis="x", rotation=0)
fig.tight_layout()
st.pyplot(fig, use_container_width=True)
plt.close(fig)

# ---------- Data table and download ----------
st.markdown("<div class='section-head'>Train records</div><div class='section-note'>Inspect individual records or download the filtered data as a CSV file.</div>", unsafe_allow_html=True)
show_cols = ["date", "train_no", "train_name", "origin", "destination", "scheduled_minutes", "actual_minutes", "delay_minutes", "on_time", "distance_km"]
display_df = filtered[show_cols].sort_values(["date", "delay_minutes"], ascending=[False, False]).copy()
display_df["date"] = display_df["date"].dt.strftime("%d %b %Y")
display_df = display_df.rename(columns={"date":"Date", "train_no":"Train no.", "train_name":"Train", "origin":"From", "destination":"To", "scheduled_minutes":"Scheduled (min)", "actual_minutes":"Actual (min)", "delay_minutes":"Delay (min)", "on_time":"On time?", "distance_km":"Distance (km)"})
st.dataframe(display_df, use_container_width=True, hide_index=True, height=360)
csv_bytes = filtered[show_cols].to_csv(index=False).encode("utf-8")
st.download_button("⬇️ Download filtered records", data=csv_bytes, file_name="railpulse_filtered_records.csv", mime="text/csv", type="primary")

# ---------- How to read / footer ----------
with st.expander("How does RailPulse calculate these insights?"):
    st.markdown("""
    - **Delay (minutes):** max(actual_minutes - scheduled_minutes, 0). Negative differences are treated as zero delay in this simplified demo.
    - **On-time rule:** a record is considered on time if its calculated delay is **10 minutes or less**. This is a project-defined rule, not an official railway standard.
    - **Average delay:** mean of the filtered delay values, calculated using NumPy.
    - **Monthly trend:** Pandas groups records by month; Matplotlib plots the average delay.
    - **Dataset:** the CSV contains generated sample records for demonstration. Values are not live railway data and should not be used for actual travel decisions.
    """)
st.markdown("<hr><div class='small-muted'>RAILPULSE · Built with Python, Streamlit, Pandas, NumPy & Matplotlib · Educational demo only</div>", unsafe_allow_html=True)