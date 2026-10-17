# DataPulse â€” Intelligent CSV Analytics

A beginner-friendly, professional data analytics dashboard built with Python and Streamlit. Upload any CSV file and instantly get interactive charts, automatic insights, anomaly detection, and downloadable reports.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

| Feature | Description |
|---|---|
| **CSV Input** | Upload files, paste URLs, or load sample data |
| **Data Dashboard** | Rows, columns, missing values, duplicates, summary statistics, KPI cards |
| **Interactive Charts** | Bar, histogram, line, and scatter plots powered by Plotly |
| **Automatic Insights** | Plain-English observations generated from your data |
| **Anomaly Detection** | Isolation Forest (Scikit-learn) to flag unusual rows |
| **Downloads** | Export cleaned CSV and text analysis reports |

---

## Tech Stack

- **Python** â€” core language
- **Streamlit** â€” web interface
- **Pandas & NumPy** â€” data analysis
- **Plotly** â€” interactive charts
- **Scikit-learn** â€” machine learning (anomaly detection)

No database, no paid APIs, no external AI â€” everything runs locally or on Streamlit Community Cloud.

---

## Project Structure

```text
DataPulse/
â”œâ”€â”€ app.py                  # Streamlit UI and dashboard
â”œâ”€â”€ analyzer.py             # Analysis engine (Pandas, NumPy, Scikit-learn)
â”œâ”€â”€ requirements.txt        # Python dependencies
â”œâ”€â”€ README.md               # This file
â”œâ”€â”€ .gitignore              # Git ignore rules
â””â”€â”€ data/
    â””â”€â”€ sample_sales.csv    # Sample dataset for testing
```

---

## Quick Start (Local)

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

## How to Test

1. **Load Data** â€” Click "Load Sample Dataset" or upload your own CSV.
2. **Dashboard** â€” Navigate to Dashboard and verify KPI cards, stats, and column types.
3. **Charts** â€” Navigate to Charts, try each chart type, and change columns.
4. **Insights** â€” Navigate to Insights and review auto-generated observations.
5. **Anomaly Detection** â€” Navigate to Anomaly Detection, select columns, and run the model.
6. **Downloads** â€” Navigate to Downloads and test CSV and report downloads.
7. **Error Handling** â€” Try uploading a non-CSV file, an empty file, or a broken URL.

---

## Deploy to Streamlit Community Cloud (Free)

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

1. Go to [Streamlit Community Cloud](https://share.streamlit.io/).
2. Sign in with your GitHub account.
3. Click **New app**.
4. Select your repository (`DataPulse`), branch (`main`), and main file (`app.py`).
5. Click **Deploy**.

Your app will be live at `https://YOUR_USERNAME-datapulse-app.streamlit.app` within a few minutes.

---

## Key Design Decisions

- **Modular architecture** â€” `analyzer.py` handles all logic; `app.py` handles the UI. Easy to test and extend.
- **No external AI** â€” All insights come from Pandas/NumPy statistical analysis, not GPT or other APIs.
- **Graceful error handling** â€” Invalid files, broken URLs, empty datasets, and missing columns are handled with clear messages.
- **Beginner-friendly code** â€” Functions are well-named, docstrings explain parameters, and comments clarify non-obvious logic.
- **Dark theme** â€” Professional look with minimal custom CSS that works on Streamlit Community Cloud.

---

## License

MIT License â€” feel free to use, modify, and share.

---

<p align="center">
  Built using Python and Streamlit
</p>