import matplotlib.colors as mcolors
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import streamlit as st

from components import insight_box
from utils import (
    ACCENT,
    BG_CHART,
    BULAN_MAP,
    CUACA_MAP,
    DIM,
    HARI_MAP,
    MUSIM_MAP,
    TEXT_COL,
    apply_dark_style,
)


# ── CHART 1: HOURLY RENTALS ───────────────────────────────────────────────────
def plot_hourly_rentals(flt_hours):
    st.markdown("**Total Penyewaan per Jam**")

    hourly_totals = flt_hours.groupby("hr")["cnt"].sum()
    peak_hour = int(hourly_totals.idxmax())
    low_hour = int(hourly_totals.idxmin())

    fig, ax = plt.subplots(figsize=(7, 4))
    apply_dark_style(ax, fig)

    colors = []
    for hour in hourly_totals.index:
        if hour == peak_hour:
            colors.append("#6366f1")
        elif hour == low_hour:
            colors.append("#f43f5e")
        else:
            colors.append(DIM)

    ax.bar(
        hourly_totals.index,
        hourly_totals.values,
        color=colors,
        width=0.7,
        zorder=3,
    )

    ax.annotate(
        f"Puncak\n{peak_hour}:00",
        xy=(peak_hour, hourly_totals[peak_hour]),
        xytext=(peak_hour + 2, hourly_totals[peak_hour] * 0.95),
        fontsize=9,
        color="#6366f1",
        fontweight="bold",
        arrowprops=dict(
            arrowstyle="->",
            color="#6366f1",
            lw=1.2,
        ),
    )

    ax.set_xlabel("Jam (0–23)", fontsize=11)
    ax.set_ylabel("Total Penyewaan", fontsize=11)
    ax.set_title(
        f"Puncak jam {peak_hour}:00 · Sepi jam {low_hour}:00",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )
    ax.set_xticks(range(0, 24, 2))

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    insight_box(
        f"""
        Pada data terpilih, jam tersibuk terjadi pada
        <strong>{peak_hour:02d}:00</strong>, sedangkan aktivitas terendah terjadi pada
        <strong>{low_hour:02d}:00</strong>. Pola ini membantu melihat jam operasional
        dengan permintaan tertinggi dan terendah.
        """
    )


# ── CHART 2: WEEKDAY HEATMAP ──────────────────────────────────────────────────
def plot_weekday_heatmap(flt_hours):
    st.markdown("**Heatmap: Jam × Hari dalam Seminggu**")

    pivot = flt_hours.groupby(["hr", "weekday"])["cnt"].mean().unstack()
    pivot.columns = [HARI_MAP.get(col, col) for col in pivot.columns]

    ordered_days = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu", "Minggu"]
    available_days = [day for day in ordered_days if day in pivot.columns]
    pivot = pivot[available_days]

    fig, ax = plt.subplots(figsize=(7, 4.3))
    fig.patch.set_facecolor(BG_CHART)
    ax.set_facecolor(BG_CHART)

    cmap = mcolors.LinearSegmentedColormap.from_list(
        "custom",
        ["#0f1117", "#2e3250", "#6366f1", "#f59e0b"],
    )

    sns.heatmap(
        pivot.T,
        ax=ax,
        cmap=cmap,
        linewidths=0.3,
        linecolor="#0f1117",
        cbar_kws={
            "shrink": 0.8,
            "label": "Rata-rata Sewa",
        },
    )

    ax.tick_params(colors=TEXT_COL, labelsize=9)
    ax.set_xlabel("Jam", fontsize=11, color=TEXT_COL)
    ax.set_ylabel("", fontsize=11, color=TEXT_COL)
    ax.set_title(
        "Rata-rata sewa per jam × hari",
        fontsize=13,
        fontweight="bold",
        color="#e8eaf0",
        pad=12,
    )

    hour_labels = list(pivot.index)
    if len(hour_labels) > 0:
        step = max(1, len(hour_labels) // 8)
        tick_positions = np.arange(len(hour_labels))[::step] + 0.5
        tick_labels = [hour_labels[i] for i in range(0, len(hour_labels), step)]

        ax.set_xticks(tick_positions)
        ax.set_xticklabels(tick_labels, color=TEXT_COL)

    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(colors=TEXT_COL, labelsize=8)
    cbar.ax.yaxis.label.set_color(TEXT_COL)

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    insight_box(
        """
        Heatmap memperlihatkan kombinasi hari dan jam dengan rata-rata penyewaan
        tertinggi. Area warna yang lebih terang menunjukkan periode dengan aktivitas
        penggunaan sepeda yang lebih tinggi.
        """
    )


# ── CHART 3: MONTHLY TREND ────────────────────────────────────────────────────
def plot_monthly_trend(flt_days):
    st.markdown("**Tren Penyewaan Bulanan (2011–2012)**")

    data = flt_days.copy()
    data["ym"] = data["dteday"].dt.to_period("M").astype(str)

    trend = data.groupby("ym")["cnt"].sum()
    labels = list(trend.index)

    fig, ax = plt.subplots(figsize=(7, 4))
    apply_dark_style(ax, fig)

    x = range(len(trend))

    ax.fill_between(
        x,
        trend.values,
        alpha=0.15,
        color=ACCENT,
    )
    ax.plot(
        x,
        trend.values,
        color=ACCENT,
        linewidth=2.5,
        zorder=5,
    )
    ax.scatter(
        x,
        trend.values,
        color=ACCENT,
        s=50,
        zorder=6,
    )

    if "2012-01" in labels:
        sep = labels.index("2012-01")
        ax.axvline(
            sep,
            color="#f59e0b",
            linestyle="--",
            alpha=0.5,
            linewidth=1.2,
        )
        ax.text(
            sep + 0.2,
            trend.values.min() * 1.02,
            "2012 →",
            color="#f59e0b",
            fontsize=9,
        )

    n = len(labels)
    tick_idx = list(range(0, n, 3))

    if n > 0 and (n - 1) not in tick_idx:
        tick_idx.append(n - 1)

    ax.set_xticks(tick_idx)
    ax.set_xticklabels(
        [labels[i] for i in tick_idx],
        rotation=30,
        ha="right",
        fontsize=8,
    )

    ax.set_ylabel("Total Penyewaan", fontsize=11)
    ax.set_title(
        "Tren penyewaan bulanan pada data terpilih",
        fontsize=13,
        fontweight="bold",
        pad=12,
    )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    insight_box(
        """
        Grafik ini menunjukkan perubahan total penyewaan dari bulan ke bulan.
        Pola kenaikan dan penurunan dapat digunakan untuk melihat kecenderungan
        musiman dalam penggunaan layanan bike sharing.
        """
    )


# ── CHART 4: USER TYPE MONTHLY ────────────────────────────────────────────────
def plot_user_type_monthly(flt_days):
    st.markdown("**Casual vs Member Terdaftar per Bulan**")

    monthly = flt_days.groupby("mnth")[["casual", "registered"]].sum()
    monthly.index = [BULAN_MAP.get(month, month) for month in monthly.index]

    fig, ax = plt.subplots(figsize=(7, 4))
    apply_dark_style(ax, fig)

    x = np.arange(len(monthly))
    width = 0.38

    ax.bar(
        x - width / 2,
        monthly["registered"],
        width,
        label="Member",
        color="#6366f1",
        zorder=3,
    )
    ax.bar(
        x + width / 2,
        monthly["casual"],
        width,
        label="Kasual",
        color="#f59e0b",
        zorder=3,
    )

    ax.set_xticks(x)
    ax.set_xticklabels(monthly.index, fontsize=9)
    ax.set_ylabel("Total Penyewaan", fontsize=11)
    ax.set_title(
        "Perbandingan pengguna member dan kasual",
        fontsize=12,
        fontweight="bold",
        pad=12,
    )
    ax.legend(
        facecolor=BG_CHART,
        edgecolor=DIM,
        labelcolor=TEXT_COL,
        fontsize=10,
    )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    insight_box(
        """
        Pengguna member dan kasual memiliki pola penggunaan yang berbeda.
        Perbandingan ini membantu melihat segmen pengguna mana yang paling
        berkontribusi terhadap total penyewaan pada setiap bulan.
        """
    )


# ── CHART 5: WEATHER AVERAGE ──────────────────────────────────────────────────
def plot_weather_average(flt_hours):
    st.markdown("**Rata-rata Penyewaan berdasarkan Cuaca**")

    weather_avg = flt_hours.groupby("weathersit")["cnt"].mean()
    weather_avg.index = [CUACA_MAP.get(i, i) for i in weather_avg.index]

    weather_order = ["Cerah", "Berawan", "Hujan Ringan", "Badai"]
    weather_avg = weather_avg.reindex(weather_order).dropna()

    color_map = {
        "Cerah": "#10b981",
        "Berawan": "#f59e0b",
        "Hujan Ringan": "#f43f5e",
        "Badai": "#6b7280",
    }

    colors = [color_map[label] for label in weather_avg.index]

    fig, ax = plt.subplots(figsize=(6, 3.8))
    apply_dark_style(ax, fig)

    bars = ax.barh(
        weather_avg.index,
        weather_avg.values,
        color=colors,
        height=0.5,
        zorder=3,
    )

    ax.invert_yaxis()
    ax.grid(axis="x", alpha=0.15, linestyle="--", zorder=0)

    for bar, value in zip(bars, weather_avg.values):
        ax.text(
            value + 2,
            bar.get_y() + bar.get_height() / 2,
            f"{value:.0f}",
            va="center",
            fontsize=10,
            color=TEXT_COL,
        )

    ax.set_xlabel("Rata-rata Penyewaan per Jam", fontsize=11)
    ax.set_title(
        "Rata-rata Penyewaan Berdasarkan Kondisi Cuaca",
        fontsize=12,
        fontweight="bold",
        pad=12,
    )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    insight_box(
        """
        Kondisi cuaca memiliki pengaruh terhadap rata-rata jumlah penyewaan.
        Cuaca yang lebih baik cenderung menghasilkan aktivitas penyewaan yang
        lebih tinggi dibandingkan kondisi cuaca buruk.
        """
    )


# ── CHART 6: SEASON TOTAL ─────────────────────────────────────────────────────
def plot_season_total(flt_days):
    st.markdown("**Total Penyewaan berdasarkan Musim**")

    season_total = flt_days.groupby("season")["cnt"].sum()
    season_total.index = [MUSIM_MAP.get(i, i) for i in season_total.index]

    peak_season = season_total.idxmax()

    colors = [ACCENT if season == peak_season else DIM for season in season_total.index]

    fig, ax = plt.subplots(figsize=(6, 3.8))
    apply_dark_style(ax, fig)

    bars = ax.bar(
        season_total.index,
        season_total.values,
        color=colors,
        width=0.5,
        zorder=3,
    )

    max_value = season_total.values.max()

    for bar, value in zip(bars, season_total.values):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            value + max_value * 0.01,
            f"{value:,}",
            ha="center",
            fontsize=9,
            color=TEXT_COL,
        )

    ax.set_ylabel("Total Penyewaan", fontsize=11)
    ax.set_title(
        f"{peak_season} menjadi musim dengan penyewaan tertinggi",
        fontsize=12,
        fontweight="bold",
        pad=12,
    )

    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    insight_box(
        f"""
        Berdasarkan data terpilih, <strong>{peak_season}</strong> memiliki total
        penyewaan tertinggi dibandingkan musim lainnya.
        """
    )