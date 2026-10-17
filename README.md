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
| **CSV Input** | `Upload files` , `paste URLs` or `load sample data` |
| **Data Dashboard** | `Rows` , `columns` , `missing values` , `duplicates` , `summary statistics` , `KPI cards` |
| **Interactive Charts** | `Bar` , `histogram` , `line` and `scatter plots powered by Plotly` |
| **Automatic Insights** | `Plain-English observations generated from your data` |
| **Anomaly Detection** | Isolation Forest (Scikit-learn) to flag unusual rows |
| **Downloads** | `Export cleaned CSV` , `anomaly results` and `text analysis reports` |

---

# Why DataPulse

Raw CSV files are usually messy: missing values, duplicate rows, and unusual records hide inside thousands of lines. DataPulse gives a quick, code-free way to inspect a dataset, clean it, and spot problems before any deeper analysis or machine learning work.

* **Saves time :** a first-pass data quality check in seconds instead of writing Pandas scripts each time
* **No coding required :** everything is point and click, so non-programmers can use it too
* **Transparent :** insights come from statistics (Pandas, NumPy, Isolation Forest), and every cleaning step is listed to the user
* **Free and private by design :** no paid APIs and no data sent to external AI services

---

# App Walkthrough

| Page | What it does |
| ---- | ------------ |
| **Load Data** | Upload a CSV, paste a URL, or use the sample dataset. Shows a preview with the row and column count. |
| **Dashboard** | Shows rows, columns, missing values, and duplicate rows, plus KPI cards, column types, a missing values table, and summary statistics. |
| **Charts** | Interactive Plotly charts (histogram, bar chart, line, scatter). Pick the columns and chart type, and hover, zoom, or export the chart. |
| **Insights** | Auto-generated plain-English observations: missing value share, duplicates, most common values, widest-spread column, and strong correlations. |
| **Anomaly Detection** | Select numeric columns, set the expected anomaly proportion, and run Isolation Forest. Results show flagged rows and the full dataset with an Anomaly flag. |
| **Downloads** | Download the cleaned CSV (duplicates removed, missing numeric values filled with the median, with every action listed), a text analysis report, or the original CSV. |

---

# #Use Cases

* **Data cleaning before analysis:** find and fix missing values and duplicates quickly
* **Exploratory data analysis (EDA):** understand distributions, categories, and correlations at a glance
* **Outlier and error spotting:** catch unusual spikes, extreme values, and suspicious records
* **Quick reporting:** export a cleaned dataset and a summary report to share
* **Learning and teaching:** students can see how statistics and Isolation Forest behave on real data

---

# #Applications

DataPulse works on any tabular CSV, so it fits many industries:

| Industry | Example Use |
| -------- | ----------- |
| **Healthcare** | Hospital operations: unusual admission spikes, extreme stay lengths, abnormal costs |
| **Banking and Finance** | Transactions: unusually large or frequent transactions and high fraud scores |
| **E-commerce** | Orders: flash-sale spikes, high return rates, delivery delays |
| **Business and HR** | Company data: department performance, revenue and cost outliers |
| **Agriculture** | Plant disease severity and crop yield records |
| **Manufacturing** | Production lines: defect counts, downtime, and quality scores |
| **Education** | Student performance and attendance records |

Note: anomalies are statistical outliers. They are not necessarily errors or fraud, so always interpret the results in context.

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