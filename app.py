import streamlit as st
import pandas as pd
import plotly.express as px
from fpdf import FPDF

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

    /* Blue Upload Icon Pill (replaces old folder emoji) */
    .upload-btn-icon {
        background-color: #2563EB;
        color: #FFFFFF;
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 10px 20px;
        border-radius: 8px;
        font-weight: 600;
        font-size: 14px;
        margin-bottom: 8px;
        cursor: pointer;
        user-select: none;
    }
    .upload-limit-text {
        font-size: 13px;
        color: #64748B;
        margin-bottom: 20px;
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

    /* The real Streamlit uploader must stay mounted (Streamlit needs it in
       the DOM to function) but it is collapsed to zero footprint so no box,
       gutter, or spacing shows up anywhere on the page. The blue "Upload"
       pill above triggers its hidden <input type="file"> directly.
       NOTE: this targets the uploader by its Streamlit data-testid directly
       rather than a wrapping <div> from st.markdown, because markdown HTML
       and widgets render as separate sibling elements in Streamlit's DOM —
       a markdown div can never actually contain a later widget call. We
       also collapse the uploader's own element-container parent so no
       padding/margin/gap is left behind. Since there is only one file
       uploader on this page, targeting the testid globally is safe. */
    div[data-testid="stFileUploader"],
    div[data-testid="stFileUploader"] * ,
    div:has(> div[data-testid="stFileUploader"]) {
        position: absolute !important;
        width: 0 !important;
        height: 0 !important;
        min-height: 0 !important;
        max-height: 0 !important;
        padding: 0 !important;
        margin: 0 !important;
        border: 0 !important;
        overflow: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        visibility: hidden !important;
    }
    /* Re-enable pointer events on just the native input so our JS can
       still .click() it programmatically even though it's visually gone. */
    div[data-testid="stFileUploader"] input[type="file"] {
        pointer-events: auto !important;
    }

    /* Data Table Toolbar: Streamlit hides the dataframe's utility icons
       (search, download, fullscreen) at opacity 0 until the user hovers.
       Force them to stay visible at all times instead.
       Using [data-testid*="Toolbar"] (attribute CONTAINS "Toolbar") rather
       than exact names, since Streamlit has renamed this testid across
       versions — this catches stElementToolbar, stDataFrameToolbar, or any
       other *Toolbar* variant regardless of the exact string. Also targets
       the dataframe's own hover-triggered wrapper classes as a second,
       independent way to force the same result in case the testid
       approach doesn't match your installed version at all. */
    div[data-testid*="Toolbar"],
    div[data-testid*="toolbar"],
    div[class*="toolbar"] {
        opacity: 1 !important;
        visibility: visible !important;
        pointer-events: auto !important;
    }
    /* stDataFrame/stDataEditor sometimes gate the toolbar's visibility on
       a parent :hover rule instead of the toolbar's own opacity - this
       forces any such parent's toolbar child to stay shown too. */
    div[data-testid="stDataFrame"] *,
    div[data-testid="stDataEditor"] * {
        opacity: 1 !important;
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

def _pdf_output_to_bytes(pdf: "FPDF") -> bytes:
    """Normalize pdf.output(dest="S") across fpdf library variants.

    fpdf2 (the actively maintained fork, recommended) returns a bytearray
    from this call, so bytes(...) on it works directly. The older classic
    `fpdf` package (PyFPDF) instead returns a plain str for the same call,
    and bytes(some_str) raises "string argument without an encoding" — which
    is the exact error this works around. Run `pip install fpdf2` (and
    uninstall plain `fpdf` if both are present) to get the actively
    maintained library; this fallback just keeps the app working either way.
    """
    raw = pdf.output(dest="S")
    if isinstance(raw, str):
        return raw.encode("latin-1", "replace")
    return bytes(raw)


def generate_pdf_report(dataframe: pd.DataFrame, title: str, max_rows: int = 200) -> bytes:
    """Render a dataframe as a simple tabular PDF using fpdf.

    The built-in core fonts only support latin-1, so any character outside
    that range (e.g. non-Latin currency symbols) is replaced rather than
    left to raise an encoding error. Row count is capped so the PDF stays a
    reasonable size and render time for large datasets.
    """
    pdf = FPDF(orientation="L", unit="mm", format="A4")
    pdf.set_auto_page_break(auto=True, margin=12)
    pdf.add_page()

    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, title.encode("latin-1", "replace").decode("latin-1"), ln=True)
    pdf.set_font("Helvetica", "", 8)
    pdf.cell(0, 6, f"{len(dataframe):,} total record(s), showing up to {max_rows}", ln=True)
    pdf.ln(3)

    col_names = [str(c) for c in dataframe.columns]
    if not col_names:
        pdf.cell(0, 8, "No columns to display.")
        return _pdf_output_to_bytes(pdf)

    usable_width = pdf.w - pdf.l_margin - pdf.r_margin
    col_width = usable_width / len(col_names)

    pdf.set_font("Helvetica", "B", 8)
    pdf.set_fill_color(37, 99, 235)
    pdf.set_text_color(255, 255, 255)
    for col in col_names:
        label = col.encode("latin-1", "replace").decode("latin-1")
        pdf.cell(col_width, 8, label[:22], border=1, fill=True)
    pdf.ln()

    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(15, 23, 42)
    for _, row in dataframe.head(max_rows).iterrows():
        for col in col_names:
            val = str(row[col]).encode("latin-1", "replace").decode("latin-1")
            pdf.cell(col_width, 7, val[:22], border=1)
        pdf.ln()

    return _pdf_output_to_bytes(pdf)


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
            <div class="upload-btn-icon" id="trigger-upload-pill">⬆️ Upload</div>
            <div class="upload-limit-text">20MB per file • CSV</div>
            <div class="upload-title">UPLOAD FILE</div>
            <div class="upload-subtext">Drag and drop your CSV file below to launch the dashboard and executive analytics.</div>
        </div>
    """, unsafe_allow_html=True)

    # The real uploader is rendered here and collapsed to zero footprint by
    # the data-testid CSS rule above (Streamlit widgets render as their own
    # sibling DOM elements, so a wrapping markdown <div> can't contain them —
    # targeting the testid directly is what actually hides it).
    uploaded_file = st.file_uploader("", type=["csv"], key="main_uploader", label_visibility="collapsed")

    if uploaded_file is not None:
        st.session_state['uploaded_file'] = uploaded_file
        st.rerun()

    # Wire the blue pill to the hidden native file input. Uses a recurring
    # attach (rather than a one-shot inline onclick) so the handler survives
    # Streamlit's re-renders of the DOM.
    #
    # IMPORTANT: this must go through components.v1.html, not st.markdown.
    # st.markdown() inserts HTML via innerHTML, and browsers never execute
    # <script> tags inserted that way (a browser security behavior) — so a
    # <script> block placed via st.markdown silently does nothing.
    # components.v1.html renders in a real iframe, where scripts do execute.
    # From inside that iframe we reach back into the main page with
    # window.parent.document to find the pill and the hidden file input.
    st.components.v1.html("""
        <script>
        (function() {
            function wireUploadPill() {
                const doc = window.parent.document;
                const pill = doc.getElementById('trigger-upload-pill');
                if (!pill || pill.dataset.wired === 'true') return;

                const fileInput = doc.querySelector('div[data-testid="stFileUploader"] input[type="file"]');
                if (!fileInput) return;

                pill.addEventListener('click', function() {
                    fileInput.click();
                });
                pill.dataset.wired = 'true';
            }
            setInterval(wireUploadPill, 500);
            wireUploadPill();
        })();
        </script>
    """, height=0, width=0)

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

    # Column & Sort Controls
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Column & Sort Controls")
    selected_columns = st.sidebar.multiselect(
        "Columns to display:",
        options=all_cols,
        default=all_cols
    )
    sort_column = st.sidebar.selectbox("Sort by:", options=all_cols, key="sort_column")
    sort_ascending = st.sidebar.radio(
        "Sort order:", options=["Ascending", "Descending"], horizontal=True
    ) == "Ascending"

    filtered_df = filtered_df.sort_values(by=sort_column, ascending=sort_ascending)
    display_df = filtered_df[selected_columns] if selected_columns else filtered_df

    # Download Buttons: CSV and PDF
    st.sidebar.markdown("---")
    st.sidebar.markdown("### Export")
    st.sidebar.download_button(
        label="Download Report (CSV)",
        data=display_df.to_csv(index=False),
        file_name=f"Data_Report_{currency_code}.csv",
        mime="text/csv"
    )
    st.sidebar.download_button(
        label="Download Report (PDF)",
        data=generate_pdf_report(display_df, f"Data Report ({currency_code})"),
        file_name=f"Data_Report_{currency_code}.pdf",
        mime="application/pdf"
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
            chart_data = filtered_df[[selected_chart]].head(30).reset_index(drop=True)
            fig = px.bar(
                chart_data, x=chart_data.index, y=selected_chart,
                title=f"{selected_chart} — Top 30 Records",
                labels={"x": "Record", selected_chart: selected_chart}
            )
        else:
            cat_counts = filtered_df[selected_chart].value_counts().head(15).reset_index()
            cat_counts.columns = [selected_chart, "Count"]
            fig = px.bar(
                cat_counts, x=selected_chart, y="Count",
                title=f"{selected_chart} — Distribution"
            )

        fig.update_layout(
            plot_bgcolor="#FFFFFF",
            paper_bgcolor="#FFFFFF",
            font=dict(family="Inter, sans-serif", color="#0F172A"),
            margin=dict(l=20, r=20, t=50, b=20),
        )
        fig.update_traces(marker_color="#2563EB")

        # scrollZoom disabled so scrolling the page over the chart doesn't
        # accidentally zoom into it.
        st.plotly_chart(fig, use_container_width=True, config={"scrollZoom": False})

        st.markdown("---")

        st.markdown("### Data Records")
        st.dataframe(display_df.head(50), use_container_width=True)

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
