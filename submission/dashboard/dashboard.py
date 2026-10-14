import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(page_title="Bike Sharing Analytics Dashboard", page_icon="🚲", layout="wide")
sns.set_theme(style="whitegrid")

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "main_data.csv")
    df = pd.read_csv(csv_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

hour_df = load_data()

with st.sidebar:
    st.title("🚲 Capital Bikeshare")
    st.markdown("**Filter Analisis Data (2011–2012)**")
    min_date = hour_df['dteday'].min().date()
    max_date = hour_df['dteday'].max().date()
    date_range = st.date_input("Pilih Rentang Tanggal:", min_value=min_date, max_value=max_date, value=[min_date, max_date])
    season_options = st.multiselect("Pilih Musim (Season):", options=hour_df['season_label'].unique(), default=hour_df['season_label'].unique())
    weather_options = st.multiselect("Pilih Kondisi Cuaca:", options=hour_df['weather_label'].unique(), default=hour_df['weather_label'].unique())
    st.markdown("---")
    st.caption("Proyek Akhir Analisis Data - Rio Alfian")

if len(date_range) == 2:
    start_date, end_date = pd.to_datetime(date_range[0]), pd.to_datetime(date_range[1])
else:
    start_date, end_date = pd.to_datetime(min_date), pd.to_datetime(max_date)

filtered_hour = hour_df[
    (hour_df['dteday'] >= start_date) &
    (hour_df['dteday'] <= end_date) &
    (hour_df['season_label'].isin(season_options)) &
    (hour_df['weather_label'].isin(weather_options))
]

filtered_day = filtered_hour.groupby(['dteday', 'season_label', 'weather_label', 'day_type'], as_index=False).agg({
    'casual': 'sum', 'registered': 'sum', 'cnt': 'sum', 'temp_c': 'mean', 'hum_pct': 'mean', 'windspeed_kmh': 'mean'
})

st.title("📊 Dashboard Analisis Penyewaan Sepeda (Capital Bikeshare)")
st.markdown(f"Menampilkan data periode **{start_date.strftime('%d %b %Y')}** hingga **{end_date.strftime('%d %b %Y')}**")

col1, col2, col3, col4 = st.columns(4)
total_rentals = int(filtered_hour['cnt'].sum())
total_registered = int(filtered_hour['registered'].sum())
total_casual = int(filtered_hour['casual'].sum())
avg_daily = float(filtered_day['cnt'].mean()) if len(filtered_day) > 0 else 0.0

col1.metric("Total Penyewaan (Unit)", f"{total_rentals:,}")
col2.metric("Pengguna Registered", f"{total_registered:,}", f"{(total_registered/total_rentals*100 if total_rentals else 0):.1f}% dari total")
col3.metric("Pengguna Casual", f"{total_casual:,}", f"{(total_casual/total_rentals*100 if total_rentals else 0):.1f}% dari total")
col4.metric("Rata-rata Penyewaan / Hari", f"{avg_daily:,.0f}")

st.markdown("---")
st.subheader("1. Dampak Musim & Kondisi Cuaca terhadap Rata-rata Penyewaan Harian")
col_a, col_b = st.columns(2)

with col_a:
    fig1, ax1 = plt.subplots(figsize=(7, 4.5))
    season_order = [s for s in ['Fall', 'Summer', 'Winter', 'Spring'] if s in filtered_day['season_label'].unique()]
    if len(filtered_day) > 0 and len(season_order) > 0:
        s_df = filtered_day.groupby('season_label')['cnt'].mean().reindex(season_order).reset_index()
        sns.barplot(data=s_df, x='season_label', y='cnt', palette='Blues_r', ax=ax1)
        for p in ax1.patches:
            ax1.annotate(f"{p.get_height():,.0f}", (p.get_x() + p.get_width()/2., p.get_height()),
                         ha='center', va='bottom', fontweight='bold', xytext=(0, 4), textcoords='offset points')
        ax1.set_ylim(0, s_df['cnt'].max() * 1.18)
    ax1.set_title("Rata-rata Penyewaan Harian per Musim", fontweight='bold')
    ax1.set_xlabel("Musim")
    ax1.set_ylabel("Rata-rata Penyewaan / Hari")
    st.pyplot(fig1)

with col_b:
    fig2, ax2 = plt.subplots(figsize=(7, 4.5))
    if len(filtered_day) > 0:
        w_df = filtered_day.groupby('weather_label')['cnt'].mean().sort_values(ascending=False).reset_index()
        sns.barplot(data=w_df, x='weather_label', y='cnt', palette='Greens_r', ax=ax2)
        for p in ax2.patches:
            ax2.annotate(f"{p.get_height():,.0f}", (p.get_x() + p.get_width()/2., p.get_height()),
                         ha='center', va='bottom', fontweight='bold', xytext=(0, 4), textcoords='offset points')
        ax2.set_ylim(0, w_df['cnt'].max() * 1.18)
    ax2.set_title("Rata-rata Penyewaan Harian Berdasarkan Cuaca", fontweight='bold')
    ax2.set_xlabel("Kondisi Cuaca")
    ax2.set_ylabel("Rata-rata Penyewaan / Hari")
    st.pyplot(fig2)

st.markdown("---")
st.subheader("2. Pola Jam Sibuk (Peak Hours) & Perbandingan Segmen Pengguna")
col_c, col_d = st.columns(2)

with col_c:
    fig3, ax3 = plt.subplots(figsize=(7.5, 4.5))
    if len(filtered_hour) > 0:
        hr_df = filtered_hour.groupby(['day_type', 'hr'])['cnt'].mean().reset_index()
        sns.lineplot(data=hr_df, x='hr', y='cnt', hue='day_type', marker='o', linewidth=2.5, ax=ax3)
        ax3.set_xticks(range(0, 24, 2))
    ax3.set_title("Tren Penyewaan per Jam: Hari Kerja vs Akhir Pekan/Libur", fontweight='bold')
    ax3.set_xlabel("Jam Operasional (00:00 - 23:00)")
    ax3.set_ylabel("Rata-rata Penyewaan / Jam")
    st.pyplot(fig3)

with col_d:
    fig4, ax4 = plt.subplots(figsize=(7.5, 4.5))
    if len(filtered_day) > 0:
        seg_df = filtered_day.groupby('day_type')[['registered', 'casual']].mean().reset_index()
        seg_melt = seg_df.melt(id_vars='day_type', value_vars=['registered', 'casual'],
                               var_name='Segmen', value_name='Rata-rata')
        sns.barplot(data=seg_melt, x='day_type', y='Rata-rata', hue='Segmen', ax=ax4)
        for p in ax4.patches:
            if p.get_height() > 0:
                ax4.annotate(f"{p.get_height():,.0f}", (p.get_x() + p.get_width()/2., p.get_height()),
                             ha='center', va='bottom', fontweight='bold', xytext=(0, 4), textcoords='offset points')
        ax4.set_ylim(0, seg_melt['Rata-rata'].max() * 1.18)
    ax4.set_title("Perbandingan Segmen Registered vs Casual per Kategori Hari", fontweight='bold')
    ax4.set_xlabel("Kategori Hari")
    ax4.set_ylabel("Rata-rata Penyewaan / Hari")
    st.pyplot(fig4)

st.markdown("---")
st.subheader("3. Analisis Lanjutan: Clustering Waktu Operasional & Suhu Udara (Non-ML)")
col_e, col_f = st.columns(2)

with col_e:
    fig5, ax5 = plt.subplots(figsize=(7.5, 4.5))
    if len(filtered_hour) > 0:
        time_order = [
            'Dini Hari (00:00 - 05:59)',
            'Pagi / Rush Hour Pagi (06:00 - 10:59)',
            'Siang (11:00 - 15:59)',
            'Sore / Rush Hour Sore (16:00 - 19:59)',
            'Malam (20:00 - 23:59)'
        ]
        tc_df = filtered_hour.groupby('time_cluster')['cnt'].mean().reindex(time_order).dropna().reset_index()
        sns.barplot(data=tc_df, y='time_cluster', x='cnt', palette='YlGnBu', ax=ax5)
        for p in ax5.patches:
            ax5.annotate(f"{p.get_width():,.1f}", (p.get_width(), p.get_y() + p.get_height()/2.),
                         ha='left', va='center', fontweight='bold', xytext=(5, 0), textcoords='offset points')
        ax5.set_xlim(0, tc_df['cnt'].max() * 1.18)
    ax5.set_title("Manual Grouping: Klaster Waktu Operasional", fontweight='bold')
    ax5.set_xlabel("Rata-rata Penyewaan / Jam")
    ax5.set_ylabel("Klaster Waktu")
    st.pyplot(fig5)

with col_f:
    fig6, ax6 = plt.subplots(figsize=(7.5, 4.5))
    if len(filtered_day) > 0:
        filtered_day['temp_bin'] = pd.cut(
            filtered_day['temp_c'],
            bins=[0, 15, 25, 41],
            labels=['Dingin (<15°C)', 'Nyaman / Ideal (15°C - 25°C)', 'Panas (>25°C)']
        )
        tb_df = filtered_day.groupby('temp_bin', observed=False)['cnt'].mean().reset_index()
        sns.barplot(data=tb_df, x='temp_bin', y='cnt', palette='coolwarm', ax=ax6)
        for p in ax6.patches:
            ax6.annotate(f"{p.get_height():,.0f}", (p.get_x() + p.get_width()/2., p.get_height()),
                         ha='center', va='bottom', fontweight='bold', xytext=(0, 4), textcoords='offset points')
        ax6.set_ylim(0, tb_df['cnt'].max() * 1.18)
    ax6.set_title("Binning Analysis: Klaster Suhu Udara Aktual", fontweight='bold')
    ax6.set_xlabel("Klaster Suhu Udara")
    ax6.set_ylabel("Rata-rata Penyewaan / Hari")
    st.pyplot(fig6)
