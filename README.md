<div align="center">

# 🚲 Bike Sharing Data Analysis Dashboard

Interactive exploratory dashboard built with **Streamlit**, **Pandas**, **Matplotlib**, and **Seaborn** to analyze bike sharing usage patterns (daily & hourly).

</div>

## 📌 Overview
This project explores the Bike Sharing dataset (day & hour level) and provides visual insights into:
* Usage statistics (max / min / mean rentals)
* Monthly and hourly rental trends
* Weekday vs weekend behavior
* Impact of weather conditions on demand
* Casual vs registered user composition across hours
* Time series of total rentals
* Basic RFM-style distribution (Recency, Frequency, Monetary proxy) for usage intensity

The dashboard helps identify peak periods, weather sensitivity, and user behavior differences for potential operational or marketing decisions.

## 🗂️ Repository Structure
```
├── Dashboard/
│   └── Dashboard.py        # Streamlit application
├── day.csv                # Daily aggregated dataset (duplicate also in Dashboard/ & Data/)
├── hour.csv               # Hourly dataset (duplicate also in Dashboard/ & Data/)
├── requirements.txt       # Python dependencies
├── notebook.ipynb         # (Optional) Exploration / experiments (if any)
└── README.md              # Project documentation
```
Note: There are duplicate copies of the CSV files in `Dashboard/` and `Data/`. You can safely consolidate them later (see Next Steps).

## 📑 Data Description (Key Fields)
| Column | Meaning (simplified) |
| ------ | --------------------- |
| dteday | Date |
| cnt | Total rental count |
| casual | Rentals by casual (non-registered) users |
| registered | Rentals by registered users |
| hr | Hour of day (hour.csv only) |
| weathersit | Weather situation code (1 Clear → 4 Severe) |
| temp / atemp | Normalized temperature / feels-like |
| hum | Humidity |
| windspeed | Normalized wind speed |

Weather code mapping used in the app:
1: Jernih (Clear), 2: Kabut (Mist), 3: Salju/Hujan Ringan (Light snow/rain), 4: Hujan Salju Berat (Heavy conditions)

## 💻 Environment Setup
Clone the repository (after it's on GitHub):
```bash
git clone https://github.com/USERNAME/analisis-data.git
cd analisis-data
```

### Option A: Using pip (simple)
```bash
python -m venv .venv
source .venv/Scripts/activate  # Windows Git Bash / PowerShell: .venv\Scripts\activate
pip install --upgrade pip
pip install -r requirements.txt
```

### Option B: Using Pipenv
```bash
pip install --user pipenv
pipenv install -r requirements.txt
pipenv shell
```

## ▶️ Run the Dashboard
From the project root:
```bash
streamlit run Dashboard/Dashboard.py
```
The script expects `day.csv` and `hour.csv` in the same directory as the script (`Dashboard/`). Current duplicates satisfy this; if you clean up later, adjust paths in the code.

Streamlit will output a local URL (e.g., http://localhost:8501) – open it in your browser.

## 📊 Visualizations Explained
1. Statistik Penyewaan: Bar chart summarizing max/min/mean for daily and hourly totals.
2. Rata-rata Penyewaan per Bulan: Seasonal demand patterns; highlights high-rental months (> 5000 avg highlighted).
3. Rata-rata Penyewaan per Jam: Diurnal usage curve; identifies commute peaks.
4. Hari Kerja vs Akhir Pekan: Compares typical demand shift on weekends.
5. Cuaca vs Penyewaan: Sensitivity of demand to weather situations.
6. Kasual vs Terdaftar per Jam: Composition (% casual vs registered) across hours.
7. Total Penyewaan dari Waktu ke Waktu: Time series showing trend / possible growth or seasonality.
8. Distribusi RFM: Histograms for Recency (days since last activity), Frequency (usage count proxy), and Monetary (total rentals) aggregated by an identifier.

## 🧪 RFM Notes
The RFM block is a simplified adaptation: 
* Recency: Days since the last recorded date per `instant` grouping.
* Frequency: Count of records per `instant`.
* Monetary: Sum of `cnt` (proxy for value contribution).
Further segmentation (scoring, clustering) can be added in future iterations.

## ✅ Requirements
See `requirements.txt`. If you add Jupyter exploration, also ensure `ipykernel` is installed for the environment.

## 🔧 Common Issues
* Matplotlib backend errors: Upgrade `streamlit` / ensure virtualenv clean.
* FileNotFoundError: Verify `day.csv` & `hour.csv` are in the same folder as `Dashboard.py` or adjust `pd.read_csv` paths.
* Caching: If data files change, use the "Rerun" button or clear cache.

## 🚀 Next Steps / Ideas
* Remove duplicate CSV copies; keep them under a single `data/` folder and update paths.
* Add unit tests for data loading & transformations.
* Add a Makefile or task runner for convenience.
* Implement RFM scoring & clustering (KMeans / segmentation) with interactive filters.
* Dockerize for reproducible deployment.

## 🤝 Contributing
Suggestions & PRs welcome. Please open an issue first for major changes.

## 📄 License
Add a license (e.g., MIT) if you plan to share publicly. (Let me know if you'd like me to add one.)

## 🙌 Acknowledgements
Dataset inspired by common Bike Sharing datasets used in data analysis tutorials.

---
Feel free to request enhancements or clarifications.
