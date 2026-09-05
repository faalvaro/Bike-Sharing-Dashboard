import os

import pandas as pd
import streamlit as st


# ── MAPPINGS ───────────────────────────────────────────────────────────────────
BULAN_MAP = {
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "Mei",
    6: "Jun",
    7: "Jul",
    8: "Agu",
    9: "Sep",
    10: "Okt",
    11: "Nov",
    12: "Des",
}

HARI_MAP = {
    0: "Minggu",
    1: "Senin",
    2: "Selasa",
    3: "Rabu",
    4: "Kamis",
    5: "Jumat",
    6: "Sabtu",
}

MUSIM_MAP = {
    1: "🌱 Semi",
    2: "☀️ Panas",
    3: "🍂 Gugur",
    4: "❄️ Dingin",
}

CUACA_MAP = {
    1: "Cerah",
    2: "Berawan",
    3: "Hujan Ringan",
    4: "Badai",
}


# ── COLOR PALETTE ──────────────────────────────────────────────────────────────
ACCENT = "#6366f1"
DIM = "#2a2d3a"
BG_CHART = "#16181f"
TEXT_COL = "#9ca3af"
GRID_COL = "#1e2130"
PALETTE = ["#6366f1", "#f59e0b", "#10b981", "#f43f5e", "#38bdf8", "#a78bfa"]


# ── LOAD DATA ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    day_path = os.path.join(project_root, "data", "day.csv")
    hour_path = os.path.join(project_root, "data", "hour.csv")

    days_df = pd.read_csv(day_path, parse_dates=["dteday"])
    hours_df = pd.read_csv(hour_path, parse_dates=["dteday"])

    return days_df, hours_df


def prepare_data(days_df, hours_df):
    days_df = days_df.copy()
    hours_df = hours_df.copy()

    days_df["nama_bulan"] = days_df["mnth"].map(BULAN_MAP)
    hours_df["nama_bulan"] = hours_df["mnth"].map(BULAN_MAP)

    return days_df, hours_df


# ── FILTER DATA ────────────────────────────────────────────────────────────────
def filter_data(
    days_df,
    hours_df,
    selected_years,
    selected_seasons,
    selected_weather,
    selected_hour,
):
    musim_inv = {v: k for k, v in MUSIM_MAP.items()}
    cuaca_inv = {v: k for k, v in CUACA_MAP.items()}

    season_keys = [musim_inv[m] for m in selected_seasons if m in musim_inv]
    weather_keys = [cuaca_inv[c] for c in selected_weather if c in cuaca_inv]
    year_keys = [year - 2011 for year in selected_years]

    def _filter_df(df, is_hour=False):
        mask = (
            df["yr"].isin(year_keys)
            & df["season"].isin(season_keys)
            & df["weathersit"].isin(weather_keys)
        )

        if is_hour:
            mask &= (df["hr"] >= selected_hour[0]) & (df["hr"] <= selected_hour[1])

        return df.loc[mask].copy()

    flt_days = _filter_df(days_df, is_hour=False)
    flt_hours = _filter_df(hours_df, is_hour=True)

    return flt_days, flt_hours


# ── KPI HELPERS ────────────────────────────────────────────────────────────────
def human_number(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.2f}M"

    if n >= 1_000:
        return f"{n / 1_000:.1f}K"

    return str(n)


def get_kpi_metrics(flt_days, flt_hours):
    total_rentals = int(flt_days["cnt"].sum())
    average_daily = round(flt_days["cnt"].mean(), 0)

    total_users = flt_days["cnt"].sum()
    if total_users == 0:
        casual_percentage = 0
        registered_percentage = 0
    else:
        casual_percentage = round(flt_days["casual"].sum() / total_users * 100, 1)
        registered_percentage = round(100 - casual_percentage, 1)

    peak_hour = int(flt_hours.groupby("hr")["cnt"].sum().idxmax())

    return {
        "total_rentals": total_rentals,
        "average_daily": average_daily,
        "casual_percentage": casual_percentage,
        "registered_percentage": registered_percentage,
        "peak_hour": peak_hour,
    }


# ── CHART STYLE ────────────────────────────────────────────────────────────────
def apply_dark_style(ax, fig):
    fig.patch.set_facecolor(BG_CHART)
    ax.set_facecolor(BG_CHART)

    ax.tick_params(colors=TEXT_COL, labelsize=10)
    ax.xaxis.label.set_color(TEXT_COL)
    ax.yaxis.label.set_color(TEXT_COL)
    ax.title.set_color("#e8eaf0")

    for spine in ax.spines.values():
        spine.set_visible(False)

    ax.yaxis.grid(True, color=GRID_COL, linewidth=0.7, linestyle="--")
    ax.set_axisbelow(True)