"""
app.py — DataPulse: Intelligent CSV Analytics
==============================================
Main Streamlit application. Handles the UI, navigation, and connects
all the analysis features from analyzer.py.

Run with: streamlit run app.py
"""

import streamlit as st
import pandas as pd
import plotly.express as px

# Import our analysis module
import analyzer

# ---------------------------------------------------------------------------
# PAGE CONFIGURATION — must be the first Streamlit command
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="DataPulse — Intelligent CSV Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------------------------
# CUSTOM CSS — minimal dark-themed styling
# ---------------------------------------------------------------------------
st.markdown("""
<style>
    /* KPI card styling */
    .kpi-card {
        background: linear-gradient(135deg, #1e1e2f 0%, #2d2d44 100%);
        border: 1px solid #3d3d5c;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        margin: 5px 0;
    }
    .kpi-card .icon { font-size: 28px; }
    .kpi-card .value {
        font-size: 26px;
        font-weight: 700;
        color: #58a6ff;
        margin: 6px 0;
    }
    .kpi-card .label {
        font-size: 13px;
        color: #8b949e;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    /* Header styling */
    .main-header {
        text-align: center;
        padding: 10px 0 5px 0;
    }
    .main-header h1 {
        background: linear-gradient(90deg, #58a6ff, #a855f7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.5rem;
        margin-bottom: 0;
    }
    .main-header p {
        color: #8b949e;
        font-size: 1.1rem;
    }

    /* Insight card */
    .insight-card {
        background: #161b22;
        border-left: 4px solid #58a6ff;
        border-radius: 8px;
        padding: 12px 16px;
        margin: 8px 0;
        font-size: 15px;
    }

    /* Section dividers */
    .section-divider {
        border-top: 1px solid #30363d;
        margin: 20px 0;
    }
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------------------------------
# HELPER FUNCTIONS
# ---------------------------------------------------------------------------

def render_kpi_card(icon: str, value, label: str):
    """Render a single KPI card using HTML."""
    if isinstance(value, (int, float)):
        if value >= 1000:
            formatted = f"{value:,.2f}"
        else:
            formatted = f"{value:.2f}"
    else:
        formatted = str(value)

    st.markdown(f"""
    <div class="kpi-card">
        <div class="icon">{icon}</div>
        <div class="value">{formatted}</div>
        <div class="label">{label}</div>
    </div>
    """, unsafe_allow_html=True)


def safe_date_column(df: pd.DataFrame):
    """Find and return the name of a date-like column, or None."""
    return analyzer._find_date_column(df)


# ---------------------------------------------------------------------------
# SIDEBAR — Navigation and Data Input
# ---------------------------------------------------------------------------

st.sidebar.markdown("## DataPulse")
st.sidebar.caption("Intelligent CSV Analytics")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate",
    [
        "Load Data",
        "Dashboard",
        "Charts",
        "Insights",
        "Anomaly Detection",
        "Downloads",
    ],
    index=0,
)

st.sidebar.markdown("---")
st.sidebar.markdown(
    "<small>Built with Python • Streamlit • Pandas • Plotly • Scikit-learn</small>",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------------------
# SESSION STATE — keeps the loaded data across page interactions
# ---------------------------------------------------------------------------
if "df" not in st.session_state:
    st.session_state.df = None

if "source_name" not in st.session_state:
    st.session_state.source_name = ""


# ===================================================================
# PAGE: LOAD DATA
# ===================================================================
if page == "Load Data":
    st.markdown("""
    <div class="main-header">
        <h1>DataPulse</h1>
        <p>Upload a CSV, paste a URL, or try our sample dataset</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(
        '<div class="section-divider"></div>',
        unsafe_allow_html=True,
    )

    tab_upload, tab_url, tab_sample = st.tabs(
        ["Upload File", "Paste URL", "Sample Data"]
    )

    # --- Tab 1: File Upload ---
    with tab_upload:
        uploaded = st.file_uploader(
            "Choose a CSV file",
            type=["csv"],
            help="Max recommended size: 50 MB",
        )

        if uploaded is not None:
            with st.spinner("Reading your file..."):
                df, error = analyzer.load_csv_file(uploaded)

            if error:
                st.error(error)
            else:
                st.session_state.df = df
                st.session_state.source_name = uploaded.name
                st.success(
                    f"Loaded {uploaded.name} — "
                    f"{len(df):,} rows × {len(df.columns)} columns"
                )

    # --- Tab 2: URL ---
    with tab_url:
        url = st.text_input(
            "Enter a direct CSV URL",
            placeholder="https://example.com/data.csv",
        )

        if st.button("Load from URL", disabled=(not url)):
            with st.spinner("Downloading CSV..."):
                df, error = analyzer.load_csv_url(url)

            if error:
                st.error(error)
            else:
                st.session_state.df = df
                st.session_state.source_name = (
                    url.split("/")[-1] or "url_data.csv"
                )
                st.success(
                    f"Loaded — {len(df):,} rows × {len(df.columns)} columns"
                )

    # --- Tab 3: Sample ---
    with tab_sample:
        st.info(
            "Load a realistic sample sales dataset to explore DataPulse features."
        )

        if st.button("Load Sample Dataset"):
            with st.spinner("Loading sample data..."):
                df, error = analyzer.load_sample_data()

            if error:
                st.error(error)
            else:
                st.session_state.df = df
                st.session_state.source_name = "sample_sales.csv"
                st.success(
                    f"Loaded sample data — "
                    f"{len(df):,} rows × {len(df.columns)} columns"
                )

    # Show a preview if data is loaded
    if st.session_state.df is not None:
        st.markdown("### Data Preview")
        st.dataframe(
            st.session_state.df.head(20),
            use_container_width=True,
        )


# ===================================================================
# PAGE: DASHBOARD
# ===================================================================
elif page == "Dashboard":
    if st.session_state.df is None:
        st.warning("No data loaded. Go to Load Data first.")
        st.stop()

    df = st.session_state.df
    overview = analyzer.get_overview(df)

    st.markdown("## Data Dashboard")
    st.caption(f"Source: {st.session_state.source_name}")

    # --- Top-level metrics ---
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Rows", f"{overview['rows']:,}")
    m2.metric("Columns", overview["cols"])
    m3.metric("Missing Values", f"{overview['missing_total']:,}")
    m4.metric("Duplicate Rows", overview["duplicate_rows"])

    st.markdown(
        '<div class="section-divider"></div>',
        unsafe_allow_html=True,
    )

    # --- KPI Cards ---
    kpis = analyzer.detect_kpis(df)

    if kpis:
        st.markdown("### Key Performance Indicators")
        kpi_cols = st.columns(len(kpis))

        for col, kpi in zip(kpi_cols, kpis):
            with col:
                render_kpi_card(
                    kpi["icon"],
                    kpi["value"],
                    kpi["label"],
                )

        st.markdown(
            '<div class="section-divider"></div>',
            unsafe_allow_html=True,
        )

    # --- Column info ---
    col_left, col_right = st.columns(2)

    with col_left:
        st.markdown("### Column Types")

        type_data = {
            "Column": list(overview["dtypes"].keys()),
            "Type": list(overview["dtypes"].values()),
        }

        st.dataframe(
            pd.DataFrame(type_data),
            use_container_width=True,
            hide_index=True,
        )

    with col_right:
        if overview["missing_by_col"]:
            st.markdown("### Missing Values")

            miss_data = {
                "Column": list(overview["missing_by_col"].keys()),
                "Missing": list(overview["missing_by_col"].values()),
                "% of Rows": [
                    f"{round(v / overview['rows'] * 100, 1)}%"
                    for v in overview["missing_by_col"].values()
                ],
            }

            st.dataframe(
                pd.DataFrame(miss_data),
                use_container_width=True,
                hide_index=True,
            )
        else:
            st.markdown("### No Missing Values")
            st.success("All cells are filled — no missing data!")

    # --- Summary statistics ---
    stats = analyzer.get_summary_statistics(df)

    if not stats.empty:
        st.markdown("### Summary Statistics")
        st.dataframe(stats, use_container_width=True)

    st.caption(f"Dataset memory usage: {overview['memory_mb']} MB")


# ===================================================================
# PAGE: INTERACTIVE CHARTS
# ===================================================================
elif page == "Charts":
    if st.session_state.df is None:
        st.warning("No data loaded. Go to Load Data first.")
        st.stop()

    df = st.session_state.df
    overview = analyzer.get_overview(df)
    num_cols = overview["numerical_cols"]
    cat_cols = overview["categorical_cols"]
    date_col = safe_date_column(df)

    st.markdown("## Interactive Charts")
    st.caption(
        "Select columns and chart types below. "
        "Charts are generated only for suitable data."
    )

    # --- Chart type selector ---
    chart_type = st.selectbox(
        "Chart Type",
        ["Bar Chart", "Histogram", "Line Chart", "Scatter Plot"],
    )

    st.markdown(
        '<div class="section-divider"></div>',
        unsafe_allow_html=True,
    )

    # --- Bar Chart ---
    if chart_type == "Bar Chart":
        if not cat_cols:
            st.info("No categorical columns found for a bar chart.")
        else:
            bar_cat = st.selectbox("Category column (X axis)", cat_cols)

            bar_val = st.selectbox(
                "Value column (Y axis) — optional",
                ["Count"] + num_cols,
            )

            if bar_val == "Count":
                chart_data = df[bar_cat].value_counts().reset_index()
                chart_data.columns = [bar_cat, "Count"]

                fig = px.bar(
                    chart_data,
                    x=bar_cat,
                    y="Count",
                    title=f"Count by {bar_cat}",
                    color=bar_cat,
                    template="plotly_dark",
                )
            else:
                chart_data = (
                    df.groupby(bar_cat)[bar_val].sum().reset_index()
                )

                fig = px.bar(
                    chart_data,
                    x=bar_cat,
                    y=bar_val,
                    title=f"Total {bar_val} by {bar_cat}",
                    color=bar_cat,
                    template="plotly_dark",
                )

            st.plotly_chart(fig, use_container_width=True)

    # --- Histogram ---
    elif chart_type == "Histogram":
        if not num_cols:
            st.info("No numerical columns found for a histogram.")
        else:
            hist_col = st.selectbox("Numerical column", num_cols)
            bins = st.slider("Number of bins", 5, 100, 30)

            fig = px.histogram(
                df,
                x=hist_col,
                nbins=bins,
                title=f"Distribution of {hist_col}",
                template="plotly_dark",
            )

            st.plotly_chart(fig, use_container_width=True)

    # --- Line Chart ---
    elif chart_type == "Line Chart":
        if date_col is None:
            st.info(
                "No date column detected for a line chart. "
                "Make sure your dataset has a column with dates."
            )
        elif not num_cols:
            st.info("No numerical columns found for a line chart.")
        else:
            line_val = st.selectbox("Value column (Y axis)", num_cols)

            temp = df.copy()
            temp[date_col] = pd.to_datetime(
                temp[date_col],
                errors="coerce",
            )
            temp = temp.dropna(subset=[date_col])
            temp = temp.sort_values(date_col)

            fig = px.line(
                temp,
                x=date_col,
                y=line_val,
                title=f"{line_val} over Time",
                template="plotly_dark",
                markers=True,
            )

            st.plotly_chart(fig, use_container_width=True)

    # --- Scatter Plot ---
    elif chart_type == "Scatter Plot":
        if len(num_cols) < 2:
            st.info("Need at least 2 numerical columns for a scatter plot.")
        else:
            sc_x = st.selectbox("X axis", num_cols)

            sc_y = st.selectbox(
                "Y axis",
                num_cols,
                index=min(1, len(num_cols) - 1),
            )

            color_col = st.selectbox(
                "Color by (optional)",
                ["None"] + cat_cols,
            )

            color = None if color_col == "None" else color_col

            fig = px.scatter(
                df,
                x=sc_x,
                y=sc_y,
                color=color,
                title=f"{sc_y} vs {sc_x}",
                template="plotly_dark",
                opacity=0.7,
            )

            st.plotly_chart(fig, use_container_width=True)


# ===================================================================
# PAGE: INSIGHTS
# ===================================================================
elif page == "Insights":
    if st.session_state.df is None:
        st.warning("No data loaded. Go to Load Data first.")
        st.stop()

    df = st.session_state.df

    st.markdown("## Automatic Insights")
    st.caption(
        "Observations generated from your data using Pandas and NumPy — "
        "no external AI APIs."
    )

    with st.spinner("Analysing your data..."):
        insights = analyzer.generate_insights(df)

    if insights:
        for insight in insights:
            st.markdown(
                f'<div class="insight-card">{insight}</div>',
                unsafe_allow_html=True,
            )
    else:
        st.info(
            "Could not generate insights for this dataset. "
            "The data may be too small or lack suitable columns."
        )

    st.markdown(
        '<div class="section-divider"></div>',
        unsafe_allow_html=True,
    )

    # Quick data preview
    st.markdown("### Data Preview")
    st.dataframe(df.head(50), use_container_width=True)


# ===================================================================
# PAGE: ANOMALY DETECTION
# ===================================================================
elif page == "Anomaly Detection":
    if st.session_state.df is None:
        st.warning("No data loaded. Go to Load Data first.")
        st.stop()

    df = st.session_state.df
    num_cols = df.select_dtypes(include="number").columns.tolist()

    st.markdown("## Anomaly Detection")
    st.caption(
        "Uses Isolation Forest (Scikit-learn) to find statistically unusual rows."
    )

    st.info(
        "Note: Unusual values are statistical outliers. They are not "
        "necessarily errors or fraud — always interpret results in context."
    )

    if not num_cols:
        st.warning("No numerical columns available for anomaly detection.")
        st.stop()

    # Column selection
    selected_cols = st.multiselect(
        "Select numerical columns to analyse",
        num_cols,
        default=num_cols[:3],
    )

    # Contamination slider
    contamination = st.slider(
        "Expected anomaly proportion",
        min_value=0.01,
        max_value=0.20,
        value=0.05,
        step=0.01,
        help="How much of your data you expect to be unusual (default 5%).",
    )

    if st.button("Run Anomaly Detection", type="primary"):
        if not selected_cols:
            st.error("Please select at least one column.")
        else:
            with st.spinner("Running Isolation Forest model..."):
                result, message = analyzer.detect_anomalies(
                    df,
                    selected_cols,
                    contamination,
                )

            if result.empty:
                st.error(message)
            else:
                st.markdown(f"### Results\n{message}")

                anomalies = result[result["Anomaly"] == True]
                normal = result[result["Anomaly"] == False]

                tab_anom, tab_all = st.tabs(
                    ["Anomalies", "All Results"]
                )

                with tab_anom:
                    if len(anomalies) > 0:
                        st.dataframe(
                            anomalies,
                            use_container_width=True,
                        )
                    else:
                        st.info(
                            "No anomalies detected with the current settings."
                        )

                with tab_all:
                    st.dataframe(
                        result,
                        use_container_width=True,
                    )

                # Scatter plot of anomalies (if 2+ columns selected)
                if len(selected_cols) >= 2:
                    st.markdown("### Anomaly Visualization")

                    fig = px.scatter(
                        result,
                        x=selected_cols[0],
                        y=selected_cols[1],
                        color="Anomaly",
                        color_discrete_map={
                            True: "#ff4444",
                            False: "#58a6ff",
                        },
                        title=(
                            f"Anomalies: {selected_cols[0]} "
                            f"vs {selected_cols[1]}"
                        ),
                        template="plotly_dark",
                        opacity=0.7,
                    )

                    st.plotly_chart(fig, use_container_width=True)

                # Download anomaly results
                csv_data = result.to_csv(index=False)

                st.download_button(
                    "Download Anomaly Results (CSV)",
                    data=csv_data,
                    file_name="datapulse_anomaly_results.csv",
                    mime="text/csv",
                )


# ===================================================================
# PAGE: DOWNLOADS
# ===================================================================
elif page == "Downloads":
    if st.session_state.df is None:
        st.warning("No data loaded. Go to Load Data first.")
        st.stop()

    df = st.session_state.df
    overview = analyzer.get_overview(df)
    insights = analyzer.generate_insights(df)

    st.markdown("## Downloads")
    st.caption("Download cleaned data and analysis reports.")

    col_left, col_right = st.columns(2)

    # --- Cleaned CSV ---
    with col_left:
        st.markdown("### Cleaned Dataset")
        cleaned, actions = analyzer.clean_data(df)

        st.markdown("**Cleaning actions performed:**")

        for action in actions:
            st.markdown(f"- {action}")

        csv_cleaned = cleaned.to_csv(index=False)

        st.download_button(
            "Download Cleaned CSV",
            data=csv_cleaned,
            file_name="datapulse_cleaned.csv",
            mime="text/csv",
            type="primary",
        )

        st.caption(
            f"Cleaned dataset: {len(cleaned):,} rows × "
            f"{len(cleaned.columns)} columns"
        )

    # --- Text Report ---
    with col_right:
        st.markdown("### Analysis Report")
        report = analyzer.generate_report(df, insights, overview)

        st.text_area("Report Preview", report, height=300)

        st.download_button(
            "Download Report (TXT)",
            data=report,
            file_name="datapulse_report.txt",
            mime="text/plain",
            type="primary",
        )

    st.markdown(
        '<div class="section-divider"></div>',
        unsafe_allow_html=True,
    )

    # --- Original data download ---
    st.markdown("### Original Dataset")
    csv_original = df.to_csv(index=False)

    st.download_button(
        "Download Original CSV",
        data=csv_original,
        file_name=f"datapulse_original_{st.session_state.source_name}",
        mime="text/csv",
    )