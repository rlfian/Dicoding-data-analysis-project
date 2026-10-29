# Bike Sharing Analytics Dashboard 🚲

Dashboard interaktif ini menyajikan hasil eksplorasi, analisis tren, dan segmentasi operasional pada **Bike Sharing Dataset (Capital Bikeshare, Washington D.C. periode 2011–2012)** sesuai standar kriteria Dicoding.

## Pertanyaan Bisnis (S.M.A.R.T Framework)
1. **Pertanyaan 1 (Pengaruh Musim & Cuaca):**  
   *Bagaimana pengaruh perubahan musim (season) dan kondisi cuaca (weather situation) terhadap rata-rata jumlah penyewaan sepeda harian (cnt) pada sistem Capital Bikeshare sepanjang periode Januari 2011 hingga Desember 2012?*
2. **Pertanyaan 2 (Pola Jam Sibuk & Segmen Pengguna):**  
   *Bagaimana perbedaan pola distribusi penyewaan sepeda per jam (hourly bike rental) antara hari kerja (working day) dan hari libur/akhir pekan (holiday/weekend), serta bagaimana karakteristik kontribusi segmen pengguna kasual (casual) dibandingkan pengguna terdaftar (registered) sepanjang periode Januari 2011 hingga Desember 2012?*

---

## Struktur Direktori
```text
submission/
├── dashboard/
│   ├── dashboard.py
│   └── main_data.csv
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

---

## Setup Environment - Terminal / Local

### 1. Buat Virtual Environment
```bash
python -m venv venv
```

### 2. Aktivasi Virtual Environment
- **Windows (PowerShell):**
  ```powershell
  .\venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt):**
  ```cmd
  .\venv\Scripts\activate.bat
  ```
- **macOS / Linux:**
  ```bash
  source venv/bin/activate
  ```

### 3. Instalasi Dependensi
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Dashboard Streamlit
```bash
streamlit run submission/dashboard/dashboard.py
```
atau jika berada di dalam folder `submission/`:
```bash
cd submission
streamlit run dashboard/dashboard.py
```

---

## Tautan Dashboard Streamlit Cloud
Dashboard telah dideploy secara publik dan dapat diakses melalui tautan berikut:  
🔗 [Bike Sharing Dashboard di Streamlit Community Cloud](https://dicoding-data-analysis-project-hbydwslqn4asa7wrqhk2v7.streamlit.app/)
