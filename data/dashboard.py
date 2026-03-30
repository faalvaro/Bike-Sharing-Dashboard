import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os # Wajib tambahin ini dul buat ngurusin path folder

# Set konfigurasi halaman
st.set_page_config(page_title="Bike Sharing Dashboard", page_icon="🚲", layout="wide")

# Load data (pakai cache biar kenceng)
@st.cache_data
def load_data():
    # Ambil jalur direktori tempat file dashboard.py ini berada
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Gabungin jalurnya sama nama file CSV
    day_path = os.path.join(current_dir, "day.csv")
    hour_path = os.path.join(current_dir, "hour.csv")
    
    days_df = pd.read_csv(day_path)
    hours_df = pd.read_csv(hour_path)
    return days_df, hours_df

try:
    days_df, hours_df = load_data()
except FileNotFoundError:
    st.error("File data tidak ditemukan. Pastikan 'day.csv' dan 'hour.csv' ada di folder yang sama dengan file dashboard ini.")
    st.stop()

# --- SIDEBAR FILTER ---
st.sidebar.title("🚲 Filter Data")

# Mengubah angka bulan jadi nama bulan
bulan_map = {1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'Mei', 6:'Jun', 7:'Jul', 8:'Agu', 9:'Sep', 10:'Okt', 11:'Nov', 12:'Des'}
hours_df['nama_bulan'] = hours_df['mnth'].map(bulan_map)
pilihan_bulan = st.sidebar.multiselect("Pilih Bulan", list(bulan_map.values()), default=list(bulan_map.values()))

selected_hour = st.sidebar.slider("Rentang Jam", 0, 23, (0, 23))

# Filter datanya
if not pilihan_bulan:
    filtered_data = hours_df.copy()
else:
    filtered_data = hours_df[(hours_df['nama_bulan'].isin(pilihan_bulan)) & 
                             (hours_df['hr'] >= selected_hour[0]) & 
                             (hours_df['hr'] <= selected_hour[1])]

# --- HEADER UTAMA ---
st.title("📊 Dashboard Analisis Bike Sharing")
st.markdown("Dashboard ini menampilkan tren penyewaan sepeda berdasarkan jam dan bulan. Gunakan filter di sebelah kiri untuk menyesuaikan data.")

# Menampilkan metrik utama
total_sewa = filtered_data['cnt'].sum()
st.metric(label="Total Penyewaan (Sesuai Filter)", value=f"{total_sewa:,}")

st.markdown("---")

# --- VISUALISASI 1: PER JAM ---
st.subheader("Tren Penyewaan per Jam")

hourly_totals = filtered_data.groupby('hr')['cnt'].sum()

if not hourly_totals.empty:
    peak_hour = hourly_totals.idxmax()
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Highlight warna McCandless Method
    colors = ["#D3D3D3" if x != peak_hour else "#1F77B4" for x in hourly_totals.index]
    
    sns.barplot(x=hourly_totals.index, y=hourly_totals.values, palette=colors, ax=ax)
    
    ax.set_title(f"Puncak Penyewaan Terjadi Pada Jam {peak_hour}:00", loc="center", fontsize=16, pad=20, fontweight='bold')
    ax.set_xlabel("Jam", fontsize=12)
    ax.set_ylabel("Total Penyewaan", fontsize=12)
    sns.despine()
    
    st.pyplot(fig)
else:
    st.warning("Data kosong untuk rentang filter ini.")

# --- VISUALISASI 2: PER BULAN ---
st.subheader("Tren Penyewaan per Bulan")

if not pilihan_bulan:
    filtered_days = days_df.copy()
else:
    days_df['nama_bulan'] = days_df['mnth'].map(bulan_map)
    filtered_days = days_df[days_df['nama_bulan'].isin(pilihan_bulan)]

monthly_data = filtered_days.groupby('mnth')['cnt'].sum()

if not monthly_data.empty:
    peak_month = monthly_data.idxmax()
    nama_bulan_puncak = bulan_map[peak_month]
    
    fig2, ax2 = plt.subplots(figsize=(12, 6))
    
    # Highlight warna McCandless Method
    colors_month = ["#D3D3D3" if x != peak_month else "#1F77B4" for x in monthly_data.index]
    x_labels = [bulan_map[m] for m in monthly_data.index]
    
    sns.barplot(x=x_labels, y=monthly_data.values, palette=colors_month, ax=ax2)
    
    ax2.set_title(f"Bulan {nama_bulan_puncak} Memiliki Total Penyewaan Tertinggi", loc="center", fontsize=16, pad=20, fontweight='bold')
    ax2.set_xlabel("Bulan", fontsize=12)
    ax2.set_ylabel("Total Penyewaan", fontsize=12)
    sns.despine()
    
    st.pyplot(fig2)
else:
    st.warning("Data kosong untuk filter ini.")

# --- TAMPILKAN DATA MENTAH ---
with st.expander("Tampilkan Data Mentah (Jam)"):
    st.dataframe(filtered_data.head())