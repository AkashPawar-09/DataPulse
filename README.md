# 📊 DataPulse — Intelligent CSV Analytics

A beginner-friendly, professional data analytics dashboard built with Python and Streamlit. Upload any CSV file and instantly get interactive charts, automatic insights, anomaly detection, and downloadable reports.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

| Feature | Description |
|---|---|
| **CSV Input** | Upload files, paste URLs, or load sample data |
| **Data Dashboard** | Rows, columns, missing values, duplicates, summary statistics, KPI cards |
| **Interactive Charts** | Bar, histogram, line, and scatter plots powered by Plotly |
| **Automatic Insights** | Plain-English observations generated from your data |
| **Anomaly Detection** | Isolation Forest (Scikit-learn) to flag unusual rows |
| **Downloads** | Export cleaned CSV and text analysis reports |

---

## 🛠️ Tech Stack

- **Python** — core language
- **Streamlit** — web interface
- **Pandas & NumPy** — data analysis
- **Plotly** — interactive charts
- **Scikit-learn** — machine learning (anomaly detection)

No database, no paid APIs, no external AI — everything runs locally or on Streamlit Community Cloud.

---

## 📁 Project Structure

```
DataPulse/
├── app.py                  # Streamlit UI and dashboard
├── analyzer.py             # Analysis engine (Pandas, NumPy, Scikit-learn)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── .gitignore              # Git ignore rules
└── data/
    └── sample_sales.csv    # Sample dataset for testing
```

---

## 🚀 Quick Start (Local)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/DataPulse.git
cd DataPulse
```

### 2. Create a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`.

---

## 🧪 How to Test

1. **Load Data** — Click "Load Sample Dataset" or upload your own CSV.
2. **Dashboard** — Navigate to 📋 Dashboard and verify KPI cards, stats, and column types.
3. **Charts** — Navigate to 📈 Charts, try each chart type, and change columns.
4. **Insights** — Navigate to 💡 Insights and review auto-generated observations.
5. **Anomaly Detection** — Navigate to 🤖 Anomaly Detection, select columns, and run the model.
6. **Downloads** — Navigate to 📥 Downloads and test CSV + report downloads.
7. **Error Handling** — Try uploading a non-CSV file, an empty file, or a broken URL.

---

## ☁️ Deploy to Streamlit Community Cloud (Free)

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit: DataPulse analytics dashboard"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/DataPulse.git
git push -u origin main
```

### Step 2: Deploy

1. Go to [share.streamlit.io](https://share.streamlit.io/).
2. Sign in with your GitHub account.
3. Click **"New app"**.
4. Select your repository (`DataPulse`), branch (`main`), and main file (`app.py`).
5. Click **"Deploy"**.

Your app will be live at `https://YOUR_USERNAME-datapulse-app.streamlit.app` within a few minutes.

---

## 📝 Key Design Decisions

- **Modular architecture** — `analyzer.py` handles all logic; `app.py` handles the UI. Easy to test and extend.
- **No external AI** — All insights come from Pandas/NumPy statistical analysis, not GPT or other APIs.
- **Graceful error handling** — Invalid files, broken URLs, empty datasets, and missing columns are all handled with clear messages.
- **Beginner-friendly code** — Functions are well-named, docstrings explain parameters, and comments clarify non-obvious logic.
- **Dark theme** — Professional look with minimal custom CSS that works on Streamlit Community Cloud.

---

## 📄 License

MIT License — feel free to use, modify, and share.

---

<p align="center">
  Built with ❤️ using Python and Streamlit
</p>

