import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import seaborn as sns
import numpy as np
import os

# ── PAGE CONFIG ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="🚲 Bike Sharing Dashboard",
    page_icon="🚲",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CUSTOM CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
}

/* Background */
.stApp {
    background-color: #0f1117;
    color: #e8eaf0;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #16181f !important;
    border-right: 1px solid #2a2d3a;
}

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 28px;
}
.kpi-card {
    background: linear-gradient(135deg, #1e2130 0%, #252840 100%);
    border: 1px solid #2e3250;
    border-radius: 16px;
    padding: 22px 24px;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent);
    border-radius: 16px 16px 0 0;
}
.kpi-label {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: #6b7280;
    margin-bottom: 8px;
}
.kpi-value {
    font-family: 'Space Mono', monospace;
    font-size: 28px;
    font-weight: 700;
    color: #ffffff;
    line-height: 1;
    margin-bottom: 4px;
}
.kpi-sub {
    font-size: 12px;
    color: #4b5563;
}

/* Section headers */
.section-header {
    font-family: 'Space Mono', monospace;
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: #6366f1;
    margin: 32px 0 16px 0;
    display: flex;
    align-items: center;
    gap: 10px;
}
.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(to right, #6366f1, transparent);
}

/* Insight box */
.insight-box {
    background: linear-gradient(135deg, #1a1f35, #1e2240);
    border-left: 3px solid #6366f1;
    border-radius: 0 12px 12px 0;
    padding: 14px 20px;
    margin-top: 12px;
    font-size: 14px;
    color: #9ca3af;
    line-height: 1.6;
}
.insight-box strong {
    color: #e8eaf0;
}

/* Plotly-style chart bg */
.chart-container {
    background: #16181f;
    border: 1px solid #2a2d3a;
    border-radius: 16px;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)

# ── LOAD DATA ──────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    day_path  = os.path.join(current_dir, "day.csv")
    hour_path = os.path.join(current_dir, "hour.csv")
    days_df  = pd.read_csv(day_path,  parse_dates=["dteday"])
    hours_df = pd.read_csv(hour_path, parse_dates=["dteday"])
    return days_df, hours_df

try:
    days_df, hours_df = load_data()
except FileNotFoundError:
    st.error("❌ File tidak ditemukan. Pastikan `day.csv` & `hour.csv` satu folder dengan `dashboard.py`.")
    st.stop()

# ── MAPPINGS ───────────────────────────────────────────────────────────────────
BULAN_MAP   = {1:'Jan',2:'Feb',3:'Mar',4:'Apr',5:'Mei',6:'Jun',
               7:'Jul',8:'Agu',9:'Sep',10:'Okt',11:'Nov',12:'Des'}
HARI_MAP    = {0:'Minggu',1:'Senin',2:'Selasa',3:'Rabu',4:'Kamis',5:'Jumat',6:'Sabtu'}
MUSIM_MAP   = {1:'🌱 Semi',2:'☀️ Panas',3:'🍂 Gugur',4:'❄️ Dingin'}
CUACA_MAP   = {1:'☀️ Cerah',2:'🌥 Berawan',3:'🌧 Hujan Ringan',4:'⛈ Badai'}

hours_df['nama_bulan'] = hours_df['mnth'].map(BULAN_MAP)
days_df['nama_bulan']  = days_df['mnth'].map(BULAN_MAP)

# ── COLOR PALETTE ──────────────────────────────────────────────────────────────
ACCENT   = "#6366f1"
DIM      = "#2a2d3a"
BG_CHART = "#16181f"
TEXT_COL = "#9ca3af"
GRID_COL = "#1e2130"
PALETTE  = ["#6366f1","#f59e0b","#10b981","#f43f5e","#38bdf8","#a78bfa"]

def apply_dark_style(ax, fig):
    fig.patch.set_facecolor(BG_CHART)
    ax.set_facecolor(BG_CHART)
    ax.tick_params(colors=TEXT_COL, labelsize=10)
    ax.xaxis.label.set_color(TEXT_COL)
    ax.yaxis.label.set_color(TEXT_COL)
    ax.title.set_color("#e8eaf0")
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.yaxis.grid(True, color=GRID_COL, linewidth=0.7, linestyle='--')
    ax.set_axisbelow(True)

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🚲 Filter Dashboard")
    st.markdown("---")

    pilihan_tahun = st.multiselect(
        "📅 Tahun", options=[2011, 2012],
        default=[2011, 2012]
    )
    pilihan_musim = st.multiselect(
        "🍃 Musim",
        options=list(MUSIM_MAP.values()),
        default=list(MUSIM_MAP.values())
    )
    pilihan_cuaca = st.multiselect(
        "🌤 Cuaca",
        options=list(CUACA_MAP.values()),
        default=list(CUACA_MAP.values())
    )
    selected_hour = st.slider("⏰ Rentang Jam", 0, 23, (0, 23))

    st.markdown("---")
    st.caption("Bike Sharing Analysis Dashboard · Dicoding")

# ── FILTER ─────────────────────────────────────────────────────────────────────
musim_inv   = {v: k for k, v in MUSIM_MAP.items()}
cuaca_inv   = {v: k for k, v in CUACA_MAP.items()}
musim_keys  = [musim_inv[m] for m in pilihan_musim if m in musim_inv]
cuaca_keys  = [cuaca_inv[c] for c in pilihan_cuaca if c in cuaca_inv]

def filter_df(df, is_hour=False):
    mask = (
        (df['yr'].isin([y - 2011 for y in pilihan_tahun])) &
        (df['season'].isin(musim_keys)) &
        (df['weathersit'].isin(cuaca_keys))
    )
    if is_hour:
        mask &= (df['hr'] >= selected_hour[0]) & (df['hr'] <= selected_hour[1])
    return df[mask]

flt_hours = filter_df(hours_df, is_hour=True)
flt_days  = filter_df(days_df,  is_hour=False)

if flt_hours.empty or flt_days.empty:
    st.warning("⚠️ Filter terlalu ketat — tidak ada data yang cocok.")
    st.stop()

# ── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-bottom:8px;">
  <span style="font-family:'Space Mono',monospace; font-size:26px; font-weight:700; color:#ffffff;">
    📊 Bike Sharing
  </span>
  <span style="font-family:'Space Mono',monospace; font-size:26px; color:#6366f1;"> Dashboard</span>
</div>
<p style="color:#6b7280; font-size:14px; margin-top:0; margin-bottom:28px;">
  Analisis pola penyewaan sepeda · Dataset 2011–2012 · Gunakan filter di sidebar untuk eksplorasi
</p>
""", unsafe_allow_html=True)

# ── KPI CARDS ──────────────────────────────────────────────────────────────────
total_cnt   = int(flt_days['cnt'].sum())
avg_daily   = round(flt_days['cnt'].mean(), 0)
pct_casual  = round(flt_days['casual'].sum() / flt_days['cnt'].sum() * 100, 1)
pct_reg     = round(100 - pct_casual, 1)
peak_h      = flt_hours.groupby('hr')['cnt'].sum().idxmax()

st.markdown(f"""
<div class="kpi-grid">
  <div class="kpi-card" style="--accent:#6366f1">
    <div class="kpi-label">Total Penyewaan</div>
    <div class="kpi-value">{total_cnt:,}</div>
    <div class="kpi-sub">Semua periode terpilih</div>
  </div>
  <div class="kpi-card" style="--accent:#f59e0b">
    <div class="kpi-label">Rata-rata / Hari</div>
    <div class="kpi-value">{avg_daily:,.0f}</div>
    <div class="kpi-sub">Sepeda per hari</div>
  </div>
  <div class="kpi-card" style="--accent:#10b981">
    <div class="kpi-label">Pengguna Kasual</div>
    <div class="kpi-value">{pct_casual}%</div>
    <div class="kpi-sub">{pct_reg}% member terdaftar</div>
  </div>
  <div class="kpi-card" style="--accent:#f43f5e">
    <div class="kpi-label">Jam Puncak</div>
    <div class="kpi-value">{peak_h:02d}:00</div>
    <div class="kpi-sub">Jam tersibuk</div>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 1 — Jam Puncak & Heatmap
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">01 — POLA HARIAN & MINGGUAN</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

# ── Chart 1: Penyewaan per Jam ────────────────────────────────────────────────
with col1:
    st.markdown("**🕐 Total Penyewaan per Jam**")
    hourly_totals = flt_hours.groupby('hr')['cnt'].sum()
    peak_hour     = hourly_totals.idxmax()
    low_hour      = hourly_totals.idxmin()

    fig, ax = plt.subplots(figsize=(7, 4))
    apply_dark_style(ax, fig)

    colors = []
    for x in hourly_totals.index:
        if x == peak_hour:   colors.append("#6366f1")
        elif x == low_hour:  colors.append("#f43f5e")
        else:                 colors.append(DIM)

    bars = ax.bar(hourly_totals.index, hourly_totals.values, color=colors,
                  width=0.7, zorder=3)

    # Annotate peak & low
    ax.annotate(f"Puncak\n{peak_hour}:00",
                xy=(peak_hour, hourly_totals[peak_hour]),
                xytext=(peak_hour + 2, hourly_totals[peak_hour] * 0.95),
                fontsize=9, color="#6366f1", fontweight='bold',
                arrowprops=dict(arrowstyle='->', color='#6366f1', lw=1.2))

    ax.set_xlabel("Jam (0–23)", fontsize=11)
    ax.set_ylabel("Total Penyewaan", fontsize=11)
    ax.set_title(f"Puncak jam {peak_hour}:00 · Sepi jam {low_hour}:00",
                 fontsize=13, fontweight='bold', pad=12)
    ax.set_xticks(range(0, 24, 2))
    plt.tight_layout()
    st.pyplot(fig)
    plt.close()

    st.markdown(f"""
    <div class="insight-box">
    💡 <strong>Insight:</strong> Dua puncak jelas terlihat — jam <strong>08:00</strong> (berangkat kerja)
    dan jam <strong>17:00</strong> (pulang kerja). Pola ini menandakan mayoritas pengguna
    adalah <strong>komuter harian</strong>, bukan rekreasi.
    </div>
    """, unsafe_allow_html=True)

# ── Chart 2: Heatmap jam × hari ───────────────────────────────────────────────
with col2:
    st.markdown("**🗓 Heatmap: Jam × Hari dalam Seminggu**")
    pivot = flt_hours.groupby(['hr','weekday'])['cnt'].mean().unstack()
    pivot.columns = [HARI_MAP[c] for c in pivot.columns]
    pivot = pivot[['Senin','Selasa','Rabu','Kamis','Jumat','Sabtu','Minggu']]

    fig2, ax2 = plt.subplots(figsize=(7, 4.3))
    fig2.patch.set_facecolor(BG_CHART)
    ax2.set_facecolor(BG_CHART)

    cmap = mcolors.LinearSegmentedColormap.from_list(
        "custom", ["#0f1117", "#2e3250", "#6366f1", "#f59e0b"])

    sns.heatmap(pivot.T, ax=ax2, cmap=cmap, linewidths=0.3, linecolor="#0f1117",
                cbar_kws={'shrink': 0.8, 'label': 'Rata-rata Sewa'})

    ax2.tick_params(colors=TEXT_COL, labelsize=9)
    ax2.set_xlabel("Jam", fontsize=11, color=TEXT_COL)
    ax2.set_ylabel("", fontsize=11, color=TEXT_COL)
    ax2.set_title("Rata-rata sewa per jam × hari", fontsize=13, fontweight='bold',
                  color="#e8eaf0", pad=12)
    ax2.set_xticks(range(0, 24, 2))
    ax2.set_xticklabels(range(0, 24, 2), color=TEXT_COL)

    cbar = ax2.collections[0].colorbar
    cbar.ax.tick_params(colors=TEXT_COL, labelsize=8)
    cbar.ax.yaxis.label.set_color(TEXT_COL)

    plt.tight_layout()
    st.pyplot(fig2)
    plt.close()

    st.markdown("""
    <div class="insight-box">
    💡 <strong>Insight:</strong> Weekday (Senin–Jumat) punya dua hot-spot jelas di jam
    <strong>07–09</strong> dan <strong>17–19</strong>. Weekend justru lebih merata
    sepanjang siang — tanda pola <strong>rekreasi</strong> yang berbeda dari komuter.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 2 — Tren Bulanan & Casual vs Registered
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">02 — TREN BULANAN & SEGMENTASI PENGGUNA</div>', unsafe_allow_html=True)

col3, col4 = st.columns([1, 1], gap="large")

# ── Chart 3: Tren 2 Tahun ─────────────────────────────────────────────────────
with col3:
    st.markdown("**📈 Tren Penyewaan Bulanan (2011–2012)**")
    flt_days['ym'] = flt_days['dteday'].dt.to_period('M').astype(str)
    trend = flt_days.groupby('ym')['cnt'].sum()

    fig3, ax3 = plt.subplots(figsize=(7, 4))
    apply_dark_style(ax3, fig3)

    x = range(len(trend))
    ax3.fill_between(x, trend.values, alpha=0.15, color=ACCENT)
    ax3.plot(x, trend.values, color=ACCENT, linewidth=2.5, zorder=5)
    ax3.scatter(x, trend.values, color=ACCENT, s=50, zorder=6)

    # Vertical line antara 2011-2012
    labels = list(trend.index)
    if '2012-01' in labels:
        sep = labels.index('2012-01')
        ax3.axvline(sep, color='#f59e0b', linestyle='--', alpha=0.5, linewidth=1.2)
        ax3.text(sep + 0.2, trend.values.min() * 1.02, '2012 →',
                 color='#f59e0b', fontsize=9)

    n = len(labels)
    tick_idx = list(range(0, n, 3)) + ([n-1] if (n-1) % 3 != 0 else [])
    ax3.set_xticks(list(tick_idx))
    ax3.set_xticklabels([labels[i] for i in tick_idx], rotation=30, ha='right', fontsize=8)

    ax3.set_ylabel("Total Penyewaan", fontsize=11)
    ax3.set_title("Pertumbuhan konsisten dari 2011 ke 2012", fontsize=13,
                  fontweight='bold', pad=12)
    plt.tight_layout()
    st.pyplot(fig3)
    plt.close()

    st.markdown("""
    <div class="insight-box">
    💡 <strong>Insight:</strong> Terjadi <strong>growth signifikan</strong> dari 2011 ke 2012 —
    hampir <strong>2× lipat</strong> di bulan yang sama. Pola musiman konsisten:
    naik dari awal tahun, puncak di pertengahan, lalu turun menjelang akhir tahun.
    </div>
    """, unsafe_allow_html=True)

# ── Chart 4: Casual vs Registered per Bulan ───────────────────────────────────
with col4:
    st.markdown("**👥 Casual vs Member Terdaftar per Bulan**")
    monthly = flt_days.groupby('mnth')[['casual','registered']].sum()
    monthly.index = [BULAN_MAP[m] for m in monthly.index]

    fig4, ax4 = plt.subplots(figsize=(7, 4))
    apply_dark_style(ax4, fig4)

    x = np.arange(len(monthly))
    w = 0.38
    ax4.bar(x - w/2, monthly['registered'], w, label='Member', color="#6366f1", zorder=3)
    ax4.bar(x + w/2, monthly['casual'],     w, label='Kasual',  color="#f59e0b", zorder=3)

    ax4.set_xticks(x)
    ax4.set_xticklabels(monthly.index, fontsize=9)
    ax4.set_ylabel("Total Penyewaan", fontsize=11)
    ax4.set_title("Member mendominasi, Kasual melonjak di musim panas", fontsize=12,
                  fontweight='bold', pad=12)
    ax4.legend(facecolor=BG_CHART, edgecolor=DIM, labelcolor=TEXT_COL, fontsize=10)
    plt.tight_layout()
    st.pyplot(fig4)
    plt.close()

    st.markdown("""
    <div class="insight-box">
    💡 <strong>Insight:</strong> Pengguna <strong>member terdaftar</strong> stabil sepanjang tahun
    karena mereka adalah komuter rutin. Pengguna <strong>kasual</strong> melonjak tajam
    di bulan <strong>Mei–Agu</strong> — mengindikasikan efek musim panas dan turis.
    </div>
    """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# ROW 3 — Cuaca & Musim
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">03 — PENGARUH CUACA & MUSIM</div>', unsafe_allow_html=True)

col5, col6 = st.columns([1, 1], gap="large")

# ── Chart 5: Pengaruh cuaca ───────────────────────────────────────────────────
with col5:
    st.markdown("**🌤 Rata-rata Penyewaan berdasarkan Cuaca**")
    weather_avg = flt_hours.groupby('weathersit')['cnt'].mean()
    weather_avg.index = [CUACA_MAP.get(i, i) for i in weather_avg.index]

    fig5, ax5 = plt.subplots(figsize=(6, 3.8))
    apply_dark_style(ax5, fig5)

    clrs = ["#10b981","#f59e0b","#f43f5e","#6b7280"][:len(weather_avg)]
    bars5 = ax5.barh(weather_avg.index, weather_avg.values, color=clrs[::-1], height=0.5, zorder=3)

    for bar, val in zip(bars5, weather_avg.values[::-1]):
        ax5.text(val + 2, bar.get_y() + bar.get_height()/2,
                 f"{val:.0f}", va='center', fontsize=10, color=TEXT_COL)

    ax5.set_xlabel("Rata-rata Penyewaan per Jam", fontsize=11)
    ax5.set_title("Cuaca cerah = 2.7× lebih banyak dari hujan", fontsize=12,
                  fontweight='bold', pad=12)
    plt.tight_layout()
    st.pyplot(fig5)
    plt.close()

# ── Chart 6: Per Musim ────────────────────────────────────────────────────────
with col6:
    st.markdown("**🌿 Total Penyewaan berdasarkan Musim**")
    season_total = flt_days.groupby('season')['cnt'].sum()
    season_total.index = [MUSIM_MAP.get(i, i) for i in season_total.index]

    fig6, ax6 = plt.subplots(figsize=(6, 3.8))
    apply_dark_style(ax6, fig6)

    peak_s = season_total.idxmax()
    clrs6  = [ACCENT if s == peak_s else DIM for s in season_total.index]
    bars6  = ax6.bar(season_total.index, season_total.values, color=clrs6,
                     width=0.5, zorder=3)

    for bar, val in zip(bars6, season_total.values):
        ax6.text(bar.get_x() + bar.get_width()/2, val + season_total.values.max()*0.01,
                 f"{val:,}", ha='center', fontsize=9, color=TEXT_COL)

    ax6.set_ylabel("Total Penyewaan", fontsize=11)
    ax6.set_title(f"Musim {peak_s} jadi puncak tertinggi", fontsize=12,
                  fontweight='bold', pad=12)
    plt.tight_layout()
    st.pyplot(fig6)
    plt.close()

# ══════════════════════════════════════════════════════════════════════════════
# ROW 4 — Data Mentah
# ══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-header">04 — DATA MENTAH</div>', unsafe_allow_html=True)

tab1, tab2 = st.tabs(["📋 Data Per Jam", "📋 Data Harian"])
with tab1:
    st.dataframe(
        flt_hours[['dteday','hr','season','weathersit','casual','registered','cnt']].head(50),
        use_container_width=True
    )
with tab2:
    st.dataframe(
        flt_days[['dteday','season','weathersit','casual','registered','cnt']].head(50),
        use_container_width=True
    )

st.markdown("""
<div style="text-align:center; color:#374151; font-size:12px; margin-top:40px; padding-top:20px; border-top:1px solid #1e2130;">
  Bike Sharing Dataset Analysis · Dicoding Data Analytics Project
</div>
""", unsafe_allow_html=True)