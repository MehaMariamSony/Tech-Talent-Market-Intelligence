import streamlit as st
import pandas as pd

# ----------------------------------------------------
# 1. PAGE SETUP
# ----------------------------------------------------
st.set_page_config(
    page_title="Tech Market Intelligence",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------------------------------------
# 2. CUSTOM UI STYLES
# ----------------------------------------------------
st.markdown("""
    <style>
    /* Global Styling */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;900&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        background-color: #F8FAFC;
        color: #0F172A;
    }

    /* Main Container Padding */
    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }

    /* Top Clean Header Bar */
    .platform-nav {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #FFFFFF;
        padding: 16px 24px;
        border-bottom: 1px solid #E2E8F0;
        margin-bottom: 24px;
        border-radius: 8px;
    }
    .platform-logo {
        font-size: 20px;
        font-weight: 900;
        letter-spacing: -0.5px;
        color: #000000;
    }
    .platform-tagline {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1px;
        color: #64748B;
        text-transform: uppercase;
    }

    /* Hero Section Banner */
    .hero-banner {
        background: linear-gradient(180deg, #E2E8F0 0%, #F8FAFC 100%);
        padding: 40px 30px;
        border-radius: 12px;
        margin-bottom: 30px;
        border: 1px solid #E2E8F0;
    }
    .hero-tag {
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 2px;
        color: #64748B;
        text-transform: uppercase;
        border-left: 3px solid #2563EB;
        padding-left: 8px;
        margin-bottom: 12px;
    }
    .hero-title {
        font-size: 36px;
        font-weight: 900;
        letter-spacing: -1px;
        text-transform: uppercase;
        color: #000000;
        line-height: 1.1;
        margin-bottom: 12px;
    }
    .hero-subtitle {
        font-size: 15px;
        color: #475569;
        max-width: 600px;
    }

    /* Streamlit Metric Cards Styling */
    div[data-testid="stMetric"] {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.03);
    }

    /* Informational Pitch Cards */
    .pitch-card {
        background-color: #EAF2F8;
        border-left: 4px solid #2563EB;
        padding: 24px;
        border-radius: 8px;
        margin-bottom: 20px;
    }
    .pitch-card h4 {
        font-size: 18px;
        font-weight: 800;
        margin-bottom: 8px;
        color: #000;
        text-transform: uppercase;
    }
    .pitch-card p {
        font-size: 14px;
        color: #475569;
        line-height: 1.6;
        margin: 0;
    }

    /* Center Upload Card & Blue Custom Dropzone Styling */
    .upload-container-card {
        background-color: #EFF6FF;
        border: 2px dashed #2563EB;
        border-radius: 16px;
        padding: 40px 20px 20px 20px;
        text-align: center;
        max-width: 800px;
        margin: 40px auto;
        box-shadow: 0 10px 25px -5px rgba(37, 99, 235, 0.1);
    }
    .upload-icon {
        font-size: 48px;
        margin-bottom: 10px;
    }
    .upload-tag {
        font-size: 13px;
        font-weight: 700;
        color: #2563EB;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }
    .upload-title {
        color: #1E3A8A;
        font-weight: 900;
        font-size: 32px;
        text-transform: uppercase;
        margin-bottom: 12px;
    }
    .upload-subtext {
        color: #3B82F6;
        font-size: 15px;
        margin-bottom: 24px;
    }

    /* Blue File Uploader Drop Zone & Button */
    div[data-testid="stFileUploader"] {
        width: 100%;
        max-width: 600px;
        margin: 0 auto;
    }
    div[data-testid="stFileUploader"] section {
        padding: 30px !important;
        background-color: #DBEAFE !important;
        border: 2px dashed #2563EB !important;
        border-radius: 12px !important;
    }
    div[data-testid="stFileUploader"] section:hover {
        background-color: #BFDBFE !important;
    }

    /* Style the Upload Button inside Streamlit file uploader to be Blue */
    div[data-testid="stFileUploader"] button {
        background-color: #2563EB !important;
        color: #FFFFFF !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 8px 16px !important;
        font-weight: 600 !important;
    }
    div[data-testid="stFileUploader"] button:hover {
        background-color: #1D4ED8 !important;
        color: #FFFFFF !important;
    }

    /* Dark Modern Footer */
    .platform-footer {
        background-color: #0A0A0A;
        color: #FFFFFF;
        padding: 24px;
        border-radius: 12px;
        margin-top: 50px;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    .platform-footer p {
        margin: 0;
        font-size: 13px;
        color: #94A3B8;
    }

    /* Clean Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        font-weight: 700;
        text-transform: uppercase;
        font-size: 13px;
        padding: 10px 20px;
        border-radius: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 3. HEADER NAV BAR
# ----------------------------------------------------
st.markdown("""
    <div class="platform-nav">
        <div class="platform-logo">TECH INTELLIGENCE</div>
        <div class="platform-tagline">Tech Talent & Market Intelligence</div>
    </div>
""", unsafe_allow_html=True)

# ----------------------------------------------------
# 4. MAIN SCREEN UPLOADER & DATA PROCESSING
# ----------------------------------------------------
if 'uploaded_file' not in st.session_state:
    st.session_state['uploaded_file'] = None

EXCHANGE_RATES = {
    "INR (₹) - Indian Rupee": ("₹", 83.5, "INR"),
    "USD ($) - US Dollar": ("$", 1.0, "USD"),
    "EUR (€) - Euro": ("€", 0.92, "EUR"),
    "GBP (£) - British Pound": ("£", 0.78, "GBP"),
    "CAD ($) - Canadian Dollar": ("$", 1.37, "CAD"),
    "AUD ($) - Australian Dollar": ("$", 1.50, "AUD"),
    "JPY (¥) - Japanese Yen": ("¥", 155.0, "JPY"),
    "SGD ($) - Singapore Dollar": ("$", 1.35, "SGD"),
    "AED - UAE Dirham": ("AED ", 3.67, "AED")
}

# Centered Blue Upload Box (Shows when no file is present)
if st.session_state['uploaded_file'] is None:
    st.markdown("""
        <div class="upload-container-card">
            <div class="upload-icon">📁</div>
            <div class="upload-title">UPLOAD FILE</div>
            <div class="upload-subtext">Drag and drop your CSV file below to launch the dashboard and executive analytics.</div>
        </div>
    """, unsafe_allow_html=True)

    col_left, col_mid, col_right = st.columns([1, 4, 1])
    with col_mid:
        uploaded_file = st.file_uploader("", type=["csv"], key="main_uploader")
        if uploaded_file is not None:
            st.session_state['uploaded_file'] = uploaded_file
            st.rerun()

# If file is present
if st.session_state['uploaded_file'] is not None:
    uploaded_file = st.session_state['uploaded_file']

    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file)

    # Sidebar Controls
    st.sidebar.markdown("### Control Panel")
    if st.sidebar.button("Upload New File"):
        st.session_state['uploaded_file'] = None
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown("### Currency Configuration")
    selected_currency = st.sidebar.selectbox(
        "Select Target Currency:",
        list(EXCHANGE_RATES.keys())
    )

    currency_symbol, conversion_rate, currency_code = EXCHANGE_RATES[selected_currency]

    # Convert Currency
    converted_df = df.copy()
    numeric_cols_raw = converted_df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    for col in numeric_cols_raw:
        converted_df[col] = converted_df[col] * conversion_rate

    rename_mapping = {}
    for col in converted_df.columns:
        if "usd" in col.lower() or "salary" in col.lower():
            new_name = col.lower().replace("salary_usd", f"Salary ({currency_code})").replace("usd", currency_code).title()
            rename_mapping[col] = new_name

    converted_df.rename(columns=rename_mapping, inplace=True)
    numeric_cols = converted_df.select_dtypes(include=['float64', 'int64']).columns.tolist()
    all_cols = converted_df.columns.tolist()

    # Data Filter
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Data Filters")
    if numeric_cols:
        main_metric = numeric_cols[0]
        min_v, max_v = float(converted_df[main_metric].min()), float(converted_df[main_metric].max())
        slider_label = f"Filter by {main_metric} ({currency_symbol})"
        selected_range = st.sidebar.slider(slider_label, min_v, max_v, (min_v, max_v))
        filtered_df = converted_df[(converted_df[main_metric] >= selected_range[0]) & (converted_df[main_metric] <= selected_range[1])]
    else:
        filtered_df = converted_df

    # Download Button
    st.sidebar.markdown("---")
    st.sidebar.download_button(
        label="Download Report (CSV)",
        data=filtered_df.to_csv(index=False),
        file_name=f"Data_Report_{currency_code}.csv",
        mime="text/csv"
    )

    # ----------------------------------------------------
    # 5. MAIN HERO BANNER
    # ----------------------------------------------------
    st.markdown(f"""
        <div class="hero-banner">
            <div class="hero-tag">DATA INTELLIGENCE</div>
            <div class="hero-title">Tech Talent Market Analysis</div>
            <div class="hero-subtitle">Real-time benchmark exploration, currency adjustments, and key metric analysis. Currently displaying data in <b>{selected_currency}</b>.</div>
        </div>
    """, unsafe_allow_html=True)

    # ----------------------------------------------------
    # 6. MAIN NAVIGATION TABS
    # ----------------------------------------------------
    tab1, tab2 = st.tabs(["Interactive Dashboard", "Executive Overview"])

    # --- TAB 1: DASHBOARD ---
    with tab1:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total Records Analyzed", f"{len(filtered_df):,}")
        col2.metric("Data Columns", f"{len(df.columns)}")

        if numeric_cols:
            max_val = filtered_df[numeric_cols[0]].max()
            col3.metric("Highest Benchmark", f"{currency_symbol}{max_val:,.0f}")
        else:
            col3.metric("Highest Benchmark", "N/A")

        col4.metric("Active Currency", currency_code)

        st.markdown("<br>", unsafe_allow_html=True)

        st.markdown("### Visual Distribution Explorer")

        selected_chart = st.selectbox("Select metric/column to plot:", all_cols)

        if selected_chart in numeric_cols:
            st.bar_chart(filtered_df[selected_chart].head(30))
        else:
            cat_counts = filtered_df[selected_chart].value_counts().head(15)
            st.bar_chart(cat_counts)

        st.markdown("---")

        st.markdown("### Data Records")
        st.dataframe(filtered_df.head(50), use_container_width=True)

    # --- TAB 2: EXECUTIVE OVERVIEW ---
    with tab2:
        st.markdown("### Executive Presentation Strategy")

        s1, s2, s3, s4 = st.tabs(["1. Overview", "2. Market Findings", "3. Financial Impact", "4. Next Steps"])

        with s1:
            st.markdown(f"""
                <div class="pitch-card">
                    <h4>Executive Summary</h4>
                    <p>This platform translates raw workforce metrics into targeted market intelligence across global regions in <b>{currency_code}</b>.</p>
                </div>
            """, unsafe_allow_html=True)

        with s2:
            st.markdown("""
                <div class="pitch-card">
                    <h4>Key Findings</h4>
                    <p>• <b>High Specialization:</b> Premium compensation centers around AI, Cloud Architecture, and Data Engineering roles.<br>• <b>Global Mobility:</b> Talent retention requires competitive regional scaling.</p>
                </div>
            """, unsafe_allow_html=True)

        with s3:
            st.markdown("""
                <div class="pitch-card">
                    <h4>Business & Value Drivers</h4>
                    <p>• Prevents overspending on compensation packages by leveraging real-time benchmarks.<br>• Optimizes allocation towards high-demand tech skill sets.</p>
                </div>
            """, unsafe_allow_html=True)

        with s4:
            st.markdown("""
                <div class="pitch-card">
                    <h4>Recommended Actions</h4>
                    <p>1. Align salary bands with converted regional benchmarks.<br>2. Shift recruitment budgets directly to high-demand skill areas.</p>
                </div>
            """, unsafe_allow_html=True)

# ----------------------------------------------------
# 7. FOOTER
# ----------------------------------------------------
st.markdown("""
    <div class="platform-footer">
        <div>
            <strong style="color: #FFFFFF; font-size: 15px;">TECH INTELLIGENCE PORTAL</strong>
        </div>
        <p>&copy; All Rights Reserved.</p>
    </div>
""", unsafe_allow_html=True)
