# Bike Sharing Analytics Dashboard 🚲

Dashboard interaktif ini menyajikan hasil analisis eksplorasi dan *clustering* pada **Bike Sharing Dataset (Capital Bikeshare, Washington D.C. periode 2011–2012)**.

## Struktur Direktori
```text
submission/
├── dashboard/
│   ├── main_data.csv
│   └── dashboard.py
├── data/
│   ├── day.csv
│   └── hour.csv
├── notebook.ipynb
├── README.md
├── requirements.txt
└── url.txt
```

## Setup Environment - Anaconda
```bash
conda create --name bike-sharing-ds python=3.10
conda activate bike-sharing-ds
pip install -r requirements.txt
```

## Setup Environment - Shell/Terminal
```bash
mkdir proyek_analisis_data
cd proyek_analisis_data
pipenv install
pipenv shell
pip install -r requirements.txt
```

## Run Streamlit App
```bash
streamlit run dashboard/dashboard.py
```
