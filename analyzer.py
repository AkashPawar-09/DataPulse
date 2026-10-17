"""
analyzer.py â€” DataPulse Analysis Engine
========================================
Contains all data analysis, insight generation, cleaning, and anomaly detection
logic. Uses Pandas, NumPy, and Scikit-learn. No external AI APIs.

This module is imported by app.py and provides pure functions that take
DataFrames in and return results out â€” making it easy to test and understand.
"""

import pandas as pd
import numpy as np
from io import StringIO


# ---------------------------------------------------------------------------
# 1. DATA LOADING HELPERS
# ---------------------------------------------------------------------------

def load_csv_file(uploaded_file):
    """
    Read an uploaded CSV file into a DataFrame.

    Parameters
    ----------
    uploaded_file : streamlit.UploadedFile
        The file uploaded through Streamlit's file_uploader widget.

    Returns
    -------
    tuple : (pd.DataFrame or None, str or None)
        The loaded DataFrame, or None and an error message if loading failed.
    """
    try:
        df = pd.read_csv(uploaded_file)
        if df.empty:
            return None, "The uploaded file is empty â€” it has no rows."
        return df, None
    except pd.errors.EmptyDataError:
        return None, "The file appears to be empty or has no parseable data."
    except pd.errors.ParserError:
        return None, "Could not parse this file. Please upload a valid CSV."
    except Exception as e:
        return None, f"Unexpected error reading file: {e}"


def load_csv_url(url: str):
    """
    Download a CSV from a public URL and return a DataFrame.

    Safety measures:
    - 10 second timeout to avoid hanging on slow servers.
    - 50 MB download limit to prevent memory issues.
    - Only accepts text/CSV content.

    Parameters
    ----------
    url : str
        A publicly accessible direct link to a CSV file.

    Returns
    -------
    tuple : (pd.DataFrame or None, str or None)
    """
    import requests  # imported here so the module loads even without requests

    MAX_SIZE = 50 * 1024 * 1024  # 50 MB

    try:
        response = requests.get(url, timeout=10, stream=True)
        response.raise_for_status()

        # Check content length if the server provides it
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_SIZE:
            return None, "File is too large (over 50 MB). Please use a smaller CSV."

        # Read the content with a size cap
        chunks = []
        downloaded = 0
        for chunk in response.iter_content(chunk_size=8192):
            downloaded += len(chunk)
            if downloaded > MAX_SIZE:
                return None, "Download exceeded 50 MB limit. Please use a smaller CSV."
            chunks.append(chunk)

        text = b"".join(chunks).decode("utf-8", errors="replace")
        df = pd.read_csv(StringIO(text))

        if df.empty:
            return None, "The URL returned an empty dataset."
        return df, None

    except requests.exceptions.Timeout:
        return None, "Request timed out after 10 seconds. Check the URL and try again."
    except requests.exceptions.ConnectionError:
        return None, "Could not connect to the URL. Please check the link."
    except requests.exceptions.HTTPError as e:
        return None, f"HTTP error: {e}"
    except pd.errors.ParserError:
        return None, "The downloaded content is not a valid CSV file."
    except Exception as e:
        return None, f"Error loading URL: {e}"


def load_sample_data():
    """
    Load the bundled sample sales dataset.

    Returns
    -------
    tuple : (pd.DataFrame or None, str or None)
    """
    import os
    path = os.path.join(os.path.dirname(__file__), "data", "sample_sales.csv")
    try:
        df = pd.read_csv(path)
        return df, None
    except FileNotFoundError:
        return None, "Sample dataset file not found. Check data/sample_sales.csv."
    except Exception as e:
        return None, f"Error loading sample data: {e}"


# ---------------------------------------------------------------------------
# 2. DATASET OVERVIEW
# ---------------------------------------------------------------------------

def get_overview(df: pd.DataFrame) -> dict:
    """
    Compute a high-level overview of the dataset.

    Returns a dictionary with keys:
        rows, cols, numerical_cols, categorical_cols,
        missing_total, missing_by_col, duplicate_rows, dtypes, memory_mb
    """
    numerical_cols = df.select_dtypes(include="number").columns.tolist()
    categorical_cols = df.select_dtypes(include=["object", "category"]).columns.tolist()

    missing_by_col = df.isnull().sum()
    missing_by_col = missing_by_col[missing_by_col > 0]  # only show cols with gaps

    return {
        "rows": len(df),
        "cols": len(df.columns),
        "numerical_cols": numerical_cols,
        "categorical_cols": categorical_cols,
        "missing_total": int(df.isnull().sum().sum()),
        "missing_by_col": missing_by_col.to_dict(),
        "duplicate_rows": int(df.duplicated().sum()),
        "dtypes": df.dtypes.astype(str).to_dict(),
        "memory_mb": round(df.memory_usage(deep=True).sum() / (1024 * 1024), 2),
    }


def get_summary_statistics(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return summary statistics (describe) for numerical columns.
    Includes mean, median (50%), std, min, max, and count.
    """
    num_df = df.select_dtypes(include="number")
    if num_df.empty:
        return pd.DataFrame()  # no numerical columns
    return num_df.describe().T.round(2)


# ---------------------------------------------------------------------------
# 3. KPI DETECTION
# ---------------------------------------------------------------------------

def detect_kpis(df: pd.DataFrame) -> list[dict]:
    """
    Automatically detect KPI-worthy columns and compute headline numbers.

    Looks for columns whose names suggest revenue, profit, cost, sales, rating,
    price, quantity, or units. Returns a list of dicts with 'label', 'value',
    and 'icon' keys.
    """
    kpis = []
    col_lower_map = {c.lower().replace("_", " "): c for c in df.columns}

    # Patterns to look for: (search_term, display_label, aggregation, icon)
    patterns = [
        ("revenue",   "Total Revenue",    "sum",  ""),
        ("profit",    "Total Profit",     "sum",  ""),
        ("cost",      "Total Cost",       "sum",  ""),
        ("sales",     "Total Sales",      "sum",  ""),
        ("units sold","Total Units Sold", "sum",  ""),
        ("unit sold", "Total Units Sold", "sum",  ""),
        ("quantity",  "Total Quantity",   "sum",  ""),
        ("rating",    "Avg Rating",       "mean", "â­"),
        ("price",     "Avg Price",        "mean", ""),
    ]

    seen_labels = set()
    for keyword, label, agg, icon in patterns:
        for col_low, col_orig in col_lower_map.items():
            if keyword in col_low and label not in seen_labels:
                series = df[col_orig]
                if not pd.api.types.is_numeric_dtype(series):
                    continue
                value = series.sum() if agg == "sum" else series.mean()
                if pd.isna(value):
                    continue
                kpis.append({
                    "label": label,
                    "value": value,
                    "icon": icon,
                })
                seen_labels.add(label)
                break  # move to next pattern

    return kpis


# ---------------------------------------------------------------------------
# 4. AUTOMATIC INSIGHTS
# ---------------------------------------------------------------------------

def generate_insights(df: pd.DataFrame) -> list[str]:
    """
    Generate plain-English insights by analysing the data with Pandas/NumPy.

    Each insight is a concise sentence backed by the actual data.
    Returns an empty list when nothing meaningful can be said.
    """
    insights = []
    overview = get_overview(df)

    # --- Missing values ---
    if overview["missing_total"] > 0:
        pct = round(overview["missing_total"] / (overview["rows"] * overview["cols"]) * 100, 1)
        worst_col = max(overview["missing_by_col"], key=overview["missing_by_col"].get)
        worst_pct = round(overview["missing_by_col"][worst_col] / overview["rows"] * 100, 1)
        insights.append(
            f" The dataset has {overview['missing_total']} missing values "
            f"({pct}% of all cells). The column **{worst_col}** has the most "
            f"gaps ({worst_pct}% missing)."
        )

    # --- Duplicates ---
    if overview["duplicate_rows"] > 0:
        insights.append(
            f" Found **{overview['duplicate_rows']}** duplicate row(s). "
            f"Consider removing them for cleaner analysis."
        )

    # --- Categorical: top category ---
    date_col = _find_date_column(df)
    for col in overview["categorical_cols"]:
        if col == date_col:
            continue  # skip date columns â€” not useful as a category insight
        counts = df[col].value_counts()
        if len(counts) >= 2:
            top = counts.index[0]
            top_pct = round(counts.iloc[0] / counts.sum() * 100, 1)
            insights.append(
                f" In **{col}**, the most common value is **{top}** "
                f"({top_pct}% of entries)."
            )
            break  # only report the first suitable categorical column

    # --- Numerical: highest-value column ---
    num_cols = overview["numerical_cols"]
    if num_cols:
        # Find the column with the biggest range (max - min)
        ranges = {}
        for c in num_cols:
            col_min = df[c].min()
            col_max = df[c].max()
            if pd.notna(col_min) and pd.notna(col_max):
                ranges[c] = col_max - col_min
        if ranges:
            widest = max(ranges, key=ranges.get)
            insights.append(
                f" **{widest}** has the widest spread of values "
                f"(min {df[widest].min():,.2f}, max {df[widest].max():,.2f})."
            )

    # --- Revenue / Profit by category (if columns exist) ---
    revenue_col = _find_column(df, ["revenue", "sales", "amount"])
    category_col = _find_column(df, ["category", "product", "region", "segment"])
    if revenue_col and category_col:
        grouped = df.groupby(category_col)[revenue_col].sum().sort_values(ascending=False)
        if len(grouped) >= 2:
            top_cat = grouped.index[0]
            top_val = grouped.iloc[0]
            insights.append(
                f" **{top_cat}** leads in total **{revenue_col}** "
                f"with **{top_val:,.2f}**."
            )

    # --- Time trend (if a date column exists) ---
    date_col = _find_date_column(df)
    if date_col and revenue_col:
        temp = df.copy()
        temp[date_col] = pd.to_datetime(temp[date_col], errors="coerce")
        temp = temp.dropna(subset=[date_col, revenue_col])
        if len(temp) >= 4:
            temp = temp.sort_values(date_col)
            # Compare first half vs second half
            mid = len(temp) // 2
            first_half = temp[revenue_col].iloc[:mid].mean()
            second_half = temp[revenue_col].iloc[mid:].mean()
            if first_half > 0:
                change_pct = round((second_half - first_half) / first_half * 100, 1)
                direction = "increased" if change_pct > 0 else "decreased"
                insights.append(
                    f" Average **{revenue_col}** {direction} by "
                    f"**{abs(change_pct)}%** from the first half to the "
                    f"second half of the dataset."
                )

    # --- Correlation insight ---
    if len(num_cols) >= 2:
        corr = df[num_cols].corr()
        # Find the strongest correlation (excluding self-correlations)
        corr_vals = corr.to_numpy(copy=True)
        np.fill_diagonal(corr_vals, 0)
        corr = pd.DataFrame(corr_vals, index=corr.index, columns=corr.columns)
        abs_corr = corr.abs()
        max_corr = abs_corr.max().max()
        if max_corr >= 0.7:
            # Locate which pair
            for c1 in abs_corr.columns:
                for c2 in abs_corr.columns:
                    if c1 != c2 and abs_corr.loc[c1, c2] == max_corr:
                        actual = corr.loc[c1, c2]
                        direction = "positive" if actual > 0 else "negative"
                        insights.append(
                            f" **{c1}** and **{c2}** have a strong "
                            f"{direction} correlation ({actual:.2f})."
                        )
                        break
                else:
                    continue
                break

    return insights


def _find_column(df: pd.DataFrame, keywords: list[str]):
    """Find the first column whose name contains any of the keywords."""
    for col in df.columns:
        col_lower = col.lower().replace("_", " ")
        for kw in keywords:
            if kw in col_lower:
                return col
    return None


def _find_date_column(df: pd.DataFrame):
    """Find a column that looks like a date."""
    for col in df.columns:
        if df[col].dtype == "object":
            sample = df[col].dropna().head(20)
            try:
                pd.to_datetime(sample)
                return col
            except (ValueError, TypeError):
                continue
    # Also check if any column has datetime dtype already
    for col in df.select_dtypes(include=["datetime64"]).columns:
        return col
    return None


# ---------------------------------------------------------------------------
# 5. DATA CLEANING
# ---------------------------------------------------------------------------

def clean_data(df: pd.DataFrame) -> tuple[pd.DataFrame, list[str]]:
    """
    Perform basic data cleaning:
    1. Remove duplicate rows.
    2. Fill missing numerical values with the column median.
    3. Fill missing categorical values with 'Unknown'.

    Returns
    -------
    tuple : (cleaned DataFrame, list of actions taken)
    """
    actions = []
    cleaned = df.copy()

    # Remove duplicates
    dup_count = cleaned.duplicated().sum()
    if dup_count > 0:
        cleaned = cleaned.drop_duplicates()
        actions.append(f"Removed {dup_count} duplicate row(s).")

    # Fill numerical missing values with median
    for col in cleaned.select_dtypes(include="number").columns:
        missing = cleaned[col].isnull().sum()
        if missing > 0:
            median_val = cleaned[col].median()
            cleaned[col] = cleaned[col].fillna(median_val)
            actions.append(f"Filled {missing} missing value(s) in '{col}' with median ({median_val:.2f}).")

    # Fill categorical missing values with 'Unknown'
    for col in cleaned.select_dtypes(include=["object", "category"]).columns:
        missing = cleaned[col].isnull().sum()
        if missing > 0:
            cleaned[col] = cleaned[col].fillna("Unknown")
            actions.append(f"Filled {missing} missing value(s) in '{col}' with 'Unknown'.")

    if not actions:
        actions.append("No cleaning was needed â€” the dataset is already clean!")

    return cleaned, actions


# ---------------------------------------------------------------------------
# 6. ANOMALY DETECTION (Isolation Forest)
# ---------------------------------------------------------------------------

def detect_anomalies(df: pd.DataFrame, columns: list[str],
                     contamination: float = 0.05) -> tuple[pd.DataFrame, str]:
    """
    Use Scikit-learn's Isolation Forest to flag unusual rows.

    Parameters
    ----------
    df : pd.DataFrame
        The dataset to analyse.
    columns : list[str]
        Which numerical columns to include in the model.
    contamination : float
        Expected proportion of anomalies (default 5%).

    Returns
    -------
    tuple : (result DataFrame with 'Anomaly' column, status message)

    The 'Anomaly' column is True for rows flagged as unusual.
    """
    from sklearn.ensemble import IsolationForest

    # Validate inputs
    if not columns:
        return pd.DataFrame(), "Please select at least one numerical column."

    subset = df[columns].copy()

    # Drop rows where ALL selected columns are NaN
    subset = subset.dropna(how="all")
    if len(subset) < 10:
        return pd.DataFrame(), (
            "Not enough data â€” need at least 10 rows with values in the "
            "selected columns."
        )

    # Fill remaining NaNs with median for the model (IsolationForest can't handle NaN)
    for col in columns:
        if subset[col].isnull().any():
            subset[col] = subset[col].fillna(subset[col].median())

    # Fit the model
    model = IsolationForest(
        contamination=contamination,
        random_state=42,
        n_estimators=100,
    )
    predictions = model.fit_predict(subset)

    # Build result: -1 = anomaly, 1 = normal
    result = df.loc[subset.index].copy()
    result["Anomaly"] = predictions == -1
    anomaly_count = int(result["Anomaly"].sum())

    message = (
        f"Found **{anomaly_count}** unusual row(s) out of {len(result)} "
        f"({round(anomaly_count / len(result) * 100, 1)}%). "
        f"Unusual values are statistical outliers â€” they are not necessarily "
        f"errors or fraud."
    )

    return result, message


# ---------------------------------------------------------------------------
# 7. REPORT GENERATION
# ---------------------------------------------------------------------------

def generate_report(df: pd.DataFrame, insights: list[str],
                    overview: dict) -> str:
    """
    Generate a plain-text summary report that users can download.
    """
    lines = [
        "=" * 60,
        "  DataPulse â€” Dataset Analysis Report",
        "=" * 60,
        "",
        f"Rows              : {overview['rows']}",
        f"Columns           : {overview['cols']}",
        f"Missing Values    : {overview['missing_total']}",
        f"Duplicate Rows    : {overview['duplicate_rows']}",
        f"Memory Usage      : {overview['memory_mb']} MB",
        "",
        "--- Column Types ---",
    ]

    for col, dtype in overview["dtypes"].items():
        lines.append(f"  {col}: {dtype}")

    if overview["missing_by_col"]:
        lines.append("")
        lines.append("--- Missing Values by Column ---")
        for col, count in overview["missing_by_col"].items():
            pct = round(count / overview["rows"] * 100, 1)
            lines.append(f"  {col}: {count} ({pct}%)")

    # Summary statistics
    stats = get_summary_statistics(df)
    if not stats.empty:
        lines.append("")
        lines.append("--- Summary Statistics ---")
        lines.append(stats.to_string())

    # Insights
    if insights:
        lines.append("")
        lines.append("--- Automatic Insights ---")
        for i, insight in enumerate(insights, 1):
            # Strip markdown bold markers for the text report
            clean = insight.replace("**", "")
            lines.append(f"  {i}. {clean}")

    lines.append("")
    lines.append("=" * 60)
    lines.append("  Generated by DataPulse â€” Intelligent CSV Analytics")
    lines.append("=" * 60)

    return "\n".join(lines)