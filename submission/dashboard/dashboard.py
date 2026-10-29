import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(
    page_title="Bike Sharing Analytics Dashboard",
    page_icon="🚲",
    layout="wide"
)

# Styling dan tema seaborn
sns.set_theme(style="whitegrid")
plt.rcParams['font.family'] = 'sans-serif'

# Konfigurasi Palet Warna (Standar Dicoding: Kategori tertinggi disorot, kategori lain netral)
PRIMARY_COLOR = "#1f77b4"
MUTED_COLOR = "#D3D3D3"
CASUAL_COLOR = "#ff7f0e"

def get_highlight_palette(values, highlight_color=PRIMARY_COLOR, muted_color=MUTED_COLOR):
    """Mengembalikan list warna yang menyorot nilai maksimum dengan warna kontras dan sisanya warna netral."""
    if len(values) == 0:
        return []
    max_val = max(values)
    return [highlight_color if v == max_val else muted_color for v in values]

@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "main_data.csv")
    df = pd.read_csv(csv_path)
    df['dteday'] = pd.to_datetime(df['dteday'])
    return df

hour_df = load_data()

# ==========================================
# SIDEBAR FILTERING
# ==========================================
with st.sidebar:
    st.title("🚲 Capital Bikeshare")
    st.markdown("### **Filter Analisis Data**")
    
    # 1. Filter Rentang Tanggal
    min_date = hour_df['dteday'].min().date()
    max_date = hour_df['dteday'].max().date()
    date_range = st.date_input(
        "Pilih Rentang Tanggal:",
        min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )
    
    # 2. Filter Musim dengan opsi Semua (Selectbox sesuai masukan reviewer)
    season_options = ["Semua Musim (All Seasons)"] + sorted(hour_df['season_label'].unique().tolist())
    selected_season = st.selectbox(
        "Pilih Musim (Season):",
        options=season_options,
        index=0,
        help="Pilih opsi 'Semua Musim' untuk membandingkan seluruh musim secara komprehensif atau pilih musim tertentu."
    )
    
    # 3. Filter Cuaca dengan opsi Semua (Selectbox sesuai masukan reviewer)
    weather_options = ["Semua Cuaca (All Weathers)"] + sorted(hour_df['weather_label'].unique().tolist())
    selected_weather = st.selectbox(
        "Pilih Kondisi Cuaca:",
        options=weather_options,
        index=0,
        help="Pilih opsi 'Semua Cuaca' untuk melihat performa di segala kondisi cuaca atau filter kondisi cuaca spesifik."
    )
    
    st.markdown("---")
    st.caption("Proyek Analisis Data: Bike Sharing Dataset")
    st.caption("Nama: **Rio Alfian** | ID Dicoding: **rio_alfianac1o**")

# Ekstraksi rentang tanggal
if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])
else:
    start_date = pd.to_datetime(min_date)
    end_date = pd.to_datetime(max_date)

# Aplikasi filter data
filtered_hour = hour_df[
    (hour_df['dteday'] >= start_date) &
    (hour_df['dteday'] <= end_date)
]

if selected_season != "Semua Musim (All Seasons)":
    filtered_hour = filtered_hour[filtered_hour['season_label'] == selected_season]

if selected_weather != "Semua Cuaca (All Weathers)":
    filtered_hour = filtered_hour[filtered_hour['weather_label'] == selected_weather]

# Agregasi data harian berdasarkan data jam terfilter
filtered_day = filtered_hour.groupby(
    ['dteday', 'season_label', 'weather_label', 'day_type'],
    as_index=False
).agg({
    'casual': 'sum',
    'registered': 'sum',
    'cnt': 'sum',
    'temp_c': 'mean',
    'hum_pct': 'mean',
    'windspeed_kmh': 'mean'
})

# ==========================================
# HEADER & BUSINESS QUESTIONS
# ==========================================
st.title("📊 Dashboard Analisis Penyewaan Sepeda (Capital Bikeshare)")
st.markdown(
    f"Analisis data historis operasional sistem penyewaan sepeda periode **{start_date.strftime('%d %b %Y')}** s.d. **{end_date.strftime('%d %b %Y')}**."
)

with st.expander("📌 **Lihat Pertanyaan Bisnis (Metode S.M.A.R.T)**", expanded=False):
    st.markdown("""
    1. **Pertanyaan 1 (Pengaruh Musim & Cuaca):**  
       *Bagaimana tren dan perbandingan rata-rata jumlah penyewaan sepeda harian (`cnt`) berdasarkan musim (*season*) dan kondisi cuaca (*weather situation*) di sistem Capital Bikeshare sepanjang periode Januari 2011 hingga Desember 2012?*  
       - **Specific:** Mengukur variasi penyewaan harian berdasarkan 4 musim dan 3 kondisi cuaca utama.
       - **Measurable:** Dihitung dari rata-rata harian (unit/hari), nilai ekstrem, serta persentase penurunan antar-kategori.
       - **Actionable:** Menjadi dasar perencanaan kuota armada aktif dan jadwal *preventive maintenance*.
       - **Relevant:** Karakteristik cuaca dan musim adalah *demand driver* eksternal paling dominan.
       - **Time-bound:** Dibatasi secara tegas pada seluruh catatan data selama 2 tahun kalender penuh (2011–2012).

    2. **Pertanyaan 2 (Pola Jam Sibuk & Segmen Pengguna):**  
       *Bagaimana perbedaan pola distribusi penyewaan sepeda per jam (*hourly bike rental*) antara hari kerja (*working day*) dan hari libur/akhir pekan (*holiday/weekend*), serta bagaimana karakteristik kontribusi segmen pengguna kasual (*casual*) dibandingkan pengguna terdaftar (*registered*) sepanjang periode 2011–2012?*  
       - **Specific:** Membedah fluktuasi 24 jam operasional pada hari kerja vs hari libur serta komposisi keanggotaan pengguna.
       - **Measurable:** Menentukan jam puncak (*peak hours*) secara numerik (unit/jam) dan persentase lonjakan pengguna kasual.
       - **Actionable:** Menjadi acuan jadwal rute truk pemindahan (*rebalancing van*) dan strategi konversi *membership*.
       - **Relevant:** Menjaga ketersediaan armada di stasiun saat jam sibuk dan meningkatkan loyalitas pelanggan.
       - **Time-bound:** Dianalisis terperinci pada 17.379 jam pengamatan selama periode 2011–2012.
    """)

# ==========================================
# METRICS SUMMARY CARDS
# ==========================================
col1, col2, col3, col4 = st.columns(4)
total_rentals = int(filtered_hour['cnt'].sum())
total_registered = int(filtered_hour['registered'].sum())
total_casual = int(filtered_hour['casual'].sum())
avg_daily = float(filtered_day['cnt'].mean()) if len(filtered_day) > 0 else 0.0

col1.metric("Total Penyewaan (Unit)", f"{total_rentals:,}")
col2.metric(
    "Pengguna Registered",
    f"{total_registered:,}",
    f"{(total_registered/total_rentals*100 if total_rentals else 0):.1f}% dari total"
)
col3.metric(
    "Pengguna Casual",
    f"{total_casual:,}",
    f"{(total_casual/total_rentals*100 if total_rentals else 0):.1f}% dari total"
)
col4.metric("Rata-rata Penyewaan / Hari", f"{avg_daily:,.0f}")

st.markdown("---")

# ==========================================
# BAGIAN 1: PERTANYAAN 1 (MUSIM & CUACA)
# ==========================================
st.subheader("1. Pengaruh Musim & Kondisi Cuaca terhadap Rata-rata Penyewaan Harian")
st.caption("Visualisasi perbandingan rata-rata unit sewa harian. Kategori dengan performa tertinggi disorot warna biru, sedangkan kategori lainnya berwarna abu-abu netral.")

col_a, col_b = st.columns(2)

with col_a:
    fig1, ax1 = plt.subplots(figsize=(7, 4.5))
    season_order = [s for s in ['Fall', 'Summer', 'Winter', 'Spring'] if s in filtered_day['season_label'].unique()]
    if len(filtered_day) > 0 and len(season_order) > 0:
        s_df = filtered_day.groupby('season_label')['cnt'].mean().reindex(season_order).dropna().reset_index()
        palette_s = get_highlight_palette(s_df['cnt'])
        sns.barplot(data=s_df, x='season_label', y='cnt', hue='season_label', palette=palette_s, legend=False, ax=ax1)
        for p in ax1.patches:
            ax1.annotate(
                f"{p.get_height():,.0f}",
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontweight='bold', xytext=(0, 4), textcoords='offset points'
            )
        ax1.set_ylim(0, s_df['cnt'].max() * 1.18)
    ax1.set_title("Rata-rata Penyewaan Harian per Musim", fontweight='bold', pad=10)
    ax1.set_xlabel("Musim (Season)", fontweight='bold')
    ax1.set_ylabel("Rata-rata Penyewaan / Hari (Unit)", fontweight='bold')
    st.pyplot(fig1)

with col_b:
    fig2, ax2 = plt.subplots(figsize=(7, 4.5))
    if len(filtered_day) > 0:
        w_df = filtered_day.groupby('weather_label')['cnt'].mean().sort_values(ascending=False).reset_index()
        palette_w = get_highlight_palette(w_df['cnt'])
        sns.barplot(data=w_df, x='weather_label', y='cnt', hue='weather_label', palette=palette_w, legend=False, ax=ax2)
        for p in ax2.patches:
            ax2.annotate(
                f"{p.get_height():,.0f}",
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontweight='bold', xytext=(0, 4), textcoords='offset points'
            )
        ax2.set_ylim(0, w_df['cnt'].max() * 1.18)
    ax2.set_title("Rata-rata Penyewaan Harian Berdasarkan Cuaca", fontweight='bold', pad=10)
    ax2.set_xlabel("Kondisi Cuaca (Weather Situation)", fontweight='bold')
    ax2.set_ylabel("Rata-rata Penyewaan / Hari (Unit)", fontweight='bold')
    st.pyplot(fig2)

st.info("""
💡 **Insight Komprehensif Pertanyaan 1:**
- **Musim Gugur (Fall)** mencatat rata-rata tertinggi sebesar **5.644 unit/hari**, sedangkan **Musim Semi (Spring)** berada di posisi terendah dengan **2.604 unit/hari** (terjadi penurunan sebesar **53,86%**).
- **Cuaca Cerah (Clear/Partly Cloudy)** menghasilkan rata-rata **4.877 unit/hari**, sedangkan **Hujan/Salju Ringan (Light Snow/Rain)** menyebabkan anjloknya permintaan hingga **63,02%** menjadi hanya **1.803 unit/hari**.
- **Signifikansi Non-Teknis:** Pengguna sangat mengutamakan kenyamanan cuaca. Penurunan drastis saat hujan/salju berarti unit sepeda menganggur (*idle assets*) dan rentan rusak jika dibiarkan di stasiun terbuka.
""")

st.markdown("---")

# ==========================================
# BAGIAN 2: PERTANYAAN 2 (JAM SIBUK & SEGMEN)
# ==========================================
st.subheader("2. Pola Jam Sibuk (Peak Hours) & Karakteristik Segmen Pengguna")
st.caption("Analisis kurva per jam 24 jam operasional serta perbandingan volume harian pengguna registered dan casual.")

col_c, col_d = st.columns(2)

with col_c:
    fig3, ax3 = plt.subplots(figsize=(7.5, 4.5))
    if len(filtered_hour) > 0:
        hr_df = filtered_hour.groupby(['day_type', 'hr'])['cnt'].mean().reset_index()
        sns.lineplot(
            data=hr_df, x='hr', y='cnt', hue='day_type',
            palette={'Hari Kerja': PRIMARY_COLOR, 'Akhir Pekan / Libur': CASUAL_COLOR},
            marker='o', linewidth=2.5, ax=ax3
        )
        ax3.set_xticks(range(0, 24, 2))
        ax3.set_ylim(0, hr_df['cnt'].max() * 1.18)
        
        # Anotasi jam sibuk jika data mencakup kedua tipe hari
        hk_data = hr_df[hr_df['day_type'] == 'Hari Kerja']
        if len(hk_data) > 0:
            pagi = hk_data[hk_data['hr'] == 8]['cnt'].values
            sore = hk_data[hk_data['hr'] == 17]['cnt'].values
            if len(pagi) > 0:
                ax3.annotate('Puncak Pagi (08:00)', xy=(8, pagi[0]), xytext=(3, pagi[0] + 50),
                             arrowprops=dict(arrowstyle='->', color=PRIMARY_COLOR, lw=1.2), fontweight='bold', color=PRIMARY_COLOR)
            if len(sore) > 0:
                ax3.annotate('Puncak Sore (17:00)', xy=(17, sore[0]), xytext=(12, sore[0] + 50),
                             arrowprops=dict(arrowstyle='->', color=PRIMARY_COLOR, lw=1.2), fontweight='bold', color=PRIMARY_COLOR)
    ax3.set_title("Tren Jam Sibuk: Hari Kerja vs Akhir Pekan/Libur", fontweight='bold', pad=10)
    ax3.set_xlabel("Jam Operasional (00:00 - 23:00)", fontweight='bold')
    ax3.set_ylabel("Rata-rata Penyewaan / Jam (Unit)", fontweight='bold')
    ax3.legend(title="Kategori Hari", frameon=True)
    st.pyplot(fig3)

with col_d:
    fig4, ax4 = plt.subplots(figsize=(7.5, 4.5))
    if len(filtered_day) > 0:
        seg_df = filtered_day.groupby('day_type')[['registered', 'casual']].mean().reset_index()
        seg_melt = seg_df.melt(
            id_vars='day_type', value_vars=['registered', 'casual'],
            var_name='Segmen', value_name='Rata-rata'
        )
        sns.barplot(
            data=seg_melt, x='day_type', y='Rata-rata', hue='Segmen',
            palette={'registered': PRIMARY_COLOR, 'casual': CASUAL_COLOR}, ax=ax4
        )
        for p in ax4.patches:
            if p.get_height() > 0:
                ax4.annotate(
                    f"{p.get_height():,.0f}",
                    (p.get_x() + p.get_width()/2., p.get_height()),
                    ha='center', va='bottom', fontweight='bold', xytext=(0, 4), textcoords='offset points'
                )
        ax4.set_ylim(0, seg_melt['Rata-rata'].max() * 1.18)
    ax4.set_title("Perbandingan Segmen Registered vs Casual per Kategori Hari", fontweight='bold', pad=10)
    ax4.set_xlabel("Kategori Hari", fontweight='bold')
    ax4.set_ylabel("Rata-rata Penyewaan / Hari (Unit)", fontweight='bold')
    ax4.legend(title="Segmen Pengguna", frameon=True)
    st.pyplot(fig4)

st.info("""
💡 **Insight Komprehensif Pertanyaan 2:**
- **Pola Hari Kerja (Bimodal):** Terkonsentrasi pada jam komuter kerja/sekolah, memuncak di pukul **08:00 (477 unit/jam)** dan **17:00 (525 unit/jam)**, didominasi mutlak oleh pengguna **registered (86,8%)**.
- **Pola Akhir Pekan (Unimodal):** Membentuk satu puncak siang-sore pukul **13:00 (373 unit/jam)** dengan durasi rekreasi tinggi hingga pukul 16:00.
- **Lonjakan Pengguna Casual (+126%):** Pengguna kasual melonjak dari rata-rata **607 unit/hari** pada hari kerja menjadi **1.371 unit/hari** pada akhir pekan/libur.
- **Signifikansi Non-Teknis:** Hari kerja adalah sarana mobilitas rutin tepat waktu, sedangkan akhir pekan adalah sarana rekreasi yang membuka peluang besar konversi *membership* baru.
""")

st.markdown("---")

# ==========================================
# BAGIAN 3: ANALISIS LANJUTAN (CLUSTERING)
# ==========================================
st.subheader("3. Analisis Lanjutan: Klaster Waktu Operasional & Suhu Udara (Non-ML)")
st.caption("Penerapan Manual Grouping dan Binning Analysis untuk segmentasi operasional logistik.")

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
        palette_tc = get_highlight_palette(tc_df['cnt'])
        sns.barplot(data=tc_df, y='time_cluster', x='cnt', hue='time_cluster', palette=palette_tc, legend=False, ax=ax5)
        for p in ax5.patches:
            ax5.annotate(
                f"{p.get_width():,.1f}",
                (p.get_width(), p.get_y() + p.get_height()/2.),
                ha='left', va='center', fontweight='bold', xytext=(5, 0), textcoords='offset points'
            )
        ax5.set_xlim(0, tc_df['cnt'].max() * 1.22)
    ax5.set_title("Klaster Waktu Operasional (Manual Grouping)", fontweight='bold', pad=10)
    ax5.set_xlabel("Rata-rata Penyewaan / Jam (Unit)", fontweight='bold')
    ax5.set_ylabel("Klaster Waktu", fontweight='bold')
    st.pyplot(fig5)

with col_f:
    fig6, ax6 = plt.subplots(figsize=(7.5, 4.5))
    if len(filtered_day) > 0:
        filtered_day_temp = filtered_day.copy()
        filtered_day_temp['temp_bin'] = pd.cut(
            filtered_day_temp['temp_c'],
            bins=[0, 15, 25, 41],
            labels=['Dingin (<15°C)', 'Nyaman / Ideal (15°C - 25°C)', 'Panas (>25°C)']
        )
        tb_df = filtered_day_temp.groupby('temp_bin', observed=False)['cnt'].mean().reset_index()
        palette_tb = get_highlight_palette(tb_df['cnt'])
        sns.barplot(data=tb_df, x='temp_bin', y='cnt', hue='temp_bin', palette=palette_tb, legend=False, ax=ax6)
        for p in ax6.patches:
            ax6.annotate(
                f"{p.get_height():,.0f}",
                (p.get_x() + p.get_width()/2., p.get_height()),
                ha='center', va='bottom', fontweight='bold', xytext=(0, 4), textcoords='offset points'
            )
        ax6.set_ylim(0, tb_df['cnt'].max() * 1.18)
    ax6.set_title("Klaster Suhu Udara Aktual (Binning Analysis)", fontweight='bold', pad=10)
    ax6.set_xlabel("Klaster Suhu Udara", fontweight='bold')
    ax6.set_ylabel("Rata-rata Penyewaan / Hari (Unit)", fontweight='bold')
    st.pyplot(fig6)

st.markdown("---")

# ==========================================
# BAGIAN 4: KESIMPULAN & REKOMENDASI BISNIS
# ==========================================
st.subheader("📋 Kesimpulan & Rekomendasi Bisnis")

col_k1, col_k2 = st.columns(2)

with col_k1:
    st.markdown("""
    #### **Kesimpulan Utama:**
    1. **Pengaruh Musim & Cuaca (Pertanyaan 1):**  
       Musim Gugur (*Fall*) adalah puncak permintaan dengan rata-rata **5.644 unit/hari**, sedangkan Musim Semi (*Spring*) terendah dengan **2.604 unit/hari** (penurunan **53,86%**). Kondisi cuaca hujan/salju ringan (*Light Snow/Rain*) menurunkan penyewaan harian sebesar **63,02%** menjadi **1.803 unit/hari** dibandingkan cuaca cerah (**4.877 unit/hari**).
    2. **Pola Jam Sibuk & Segmen Pengguna (Pertanyaan 2):**  
       Hari kerja memiliki pola bimodal komuter yang memuncak pada jam **08:00 (477 unit/jam)** dan **17:00 (525 unit/jam)** didominasi oleh pengguna *registered* (**86,8%**). Akhir pekan memiliki pola unimodal rekreasi dengan puncak pada jam **13:00 (373 unit/jam)** disertai lonjakan pengguna *casual* sebesar **+126,05%**.
    """)

with col_k2:
    st.markdown("""
    #### **Rekomendasi Bisnis Actionable:**
    - **Manajemen Armada & Overhaul Musiman:**  
      Jadwalkan pemeliharaan besar (*overhaul*) pada Musim Semi dan saat suhu dingin (<15°C) saat permintaan turun 53,86%. Tarik 30%–40% armada ke gudang tertutup saat ada peringatan cuaca hujan/salju.
    - **Smart Rebalancing Logistik:**  
      Operasikan truk redistribusi pada klaster **Dini Hari (04:00–05:59)** ke permukiman sebelum jam 08:00, dan pukul **14:00–15:30** ke perkantoran sebelum jam 17:00.
    - **Weekend Conversion Campaign:**  
      Tawarkan paket diskon *Weekend Pass* yang menyertakan voucher potongan pendaftaran *Annual Membership* guna mengonversi tingginya volume pengguna kasual di akhir pekan.
    """)
