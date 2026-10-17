# DataPulse: Intelligent CSV Analytics

A beginner-friendly data analytics dashboard built with Python and Streamlit. Upload any CSV file and instantly get interactive charts, automatic insights, anomaly detection, and downloadable reports.

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Streamlit](https://img.shields.io/badge/Streamlit-1.32%2B-red?logo=streamlit)
![License](https://img.shields.io/badge/License-MIT-green)

---

# Live Demo

Try the app online: [https://datapulse-web.streamlit.app/](https://datapulse-web.streamlit.app/)

---

# Features

| Feature | Description |
| ------- | ----------- |
| **CSV Input** | Upload files, paste URLs, or load sample data |
| **Data Dashboard** | Rows, columns, missing values, duplicates, summary statistics, KPI cards |
| **Interactive Charts** | Bar, histogram, line, and scatter plots powered by Plotly |
| **Automatic Insights** | Plain-English observations generated from your data |
| **Anomaly Detection** | Isolation Forest (Scikit-learn) to flag unusual rows |
| **Downloads** | Export cleaned CSV, anomaly results, and text analysis reports |

---

# Tech Stack

* **Python**: core language
* **Streamlit**: web interface
* **Pandas & NumPy**: data analysis
* **Plotly**: interactive charts
* **Scikit-learn**: machine learning (anomaly detection)
* **Requests**: loading CSV files from URLs

No database, no paid APIs, no external AI. Everything runs locally.

---

# Project Structure

```
DataPulse/
├── .devcontainer/
│   └── devcontainer.json    # Dev container configuration
├── data/
│   └── sample_sales.csv     # Sample dataset for testing
├── analyzer.py              # Analysis engine (Pandas, NumPy, Scikit-learn)
├── main.py                  # Streamlit UI and dashboard
├── requirements.txt         # Python dependencies
├── .gitignore               # Git ignore rules
└── README.md                # Project documentation
```

---

# Quick Start

### 1. Clone the repository

```
git clone https://github.com/AkashPawar-09/DataPulse.git
cd DataPulse
```

### 2. Create a virtual environment

**Windows (PowerShell):**

```
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

### 4. Run the application

```
streamlit run main.py
```

The app will open in your browser at `http://localhost:8501`.

---

# How to Test

1. **Load Data**: Click "Load Sample Dataset" or upload your own CSV.
2. **Dashboard**: Verify KPI cards, summary statistics, and column types.
3. **Charts**: Try each chart type and change the selected columns.
4. **Insights**: Review the auto-generated observations.
5. **Anomaly Detection**: Select columns and run the model.
6. **Downloads**: Test the cleaned CSV and report downloads.
7. **Error Handling**: Try a non-CSV file, an empty file, or a broken URL.

---

# Key Design Decisions

* **Modular architecture**: `analyzer.py` handles all logic and `main.py` handles the UI, which makes the code easy to test and extend.
* **No external AI**: All insights come from Pandas and NumPy statistical analysis, not GPT or other APIs.
* **Graceful error handling**: Invalid files, broken URLs, empty datasets, and missing columns are handled with clear messages.
* **Beginner-friendly code**: Functions are well-named, docstrings explain parameters, and comments clarify non-obvious logic.
* **Dark theme**: Professional look with minimal custom CSS.

---

# License

MIT License. Feel free to use, modify, and share.

---

Built with Python and Streamlit.