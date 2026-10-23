"""
================================================================================
EXPERIMENT 5: AUTOMATED LEGAL DOCUMENT ANALYZER (STREAMLIT WEB APP)
================================================================================
Interactive Dashboard providing:
1. File upload (.txt, .pdf) & Kaggle dataset browser
2. Real-time preprocessing inspection & section detection
3. GPT-4 Legal Analysis & Summarization
4. Interactive clause exploration
5. One-click report download
================================================================================
"""

import os
import sys
import streamlit as st

# Configure page
st.set_page_config(
    page_title="Automated Legal Document Analyzer | GPT-4",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Add local path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.file_handler import load_document, save_analysis_report
from src.preprocessor import preprocess_document
from src.analyzer import LegalDocumentAnalyzer
from src.prompt_builder import build_analysis_prompt

# Custom Styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .metric-card {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 8px;
        padding: 1rem;
        margin-bottom: 1rem;
    }
    .summary-box {
        background-color: #F0FDF4;
        border-left: 5px solid #22C55E;
        padding: 1.2rem;
        border-radius: 4px;
        font-family: monospace;
        white-space: pre-wrap;
    }
    .clause-card {
        background-color: #F1F5F9;
        border-left: 4px solid #3B82F6;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 0.8rem;
    }
</style>
""", unsafe_allow_html=True)


def init_session():
    if "raw_text" not in st.session_state:
        st.session_state.raw_text = None
    if "metadata" not in st.session_state:
        st.session_state.metadata = None
    if "preprocessed" not in st.session_state:
        st.session_state.preprocessed = None
    if "analysis" not in st.session_state:
        st.session_state.analysis = None


init_session()

# Sidebar: Controls & Dataset Selection
with st.sidebar:
    st.image("https://img.icons8.com/color/96/scales--v1.png", width=64)
    st.markdown("### ⚖️ Legal Analyzer")
    st.caption("Experiment 5 - GPT-4 Document Intelligence")

    st.markdown("---")
    st.markdown("#### 1. Input Source")
    input_mode = st.radio(
        "Choose document source:",
        ["Kaggle CUAD Dataset", "Upload .txt / .pdf", "Manual Text Input"],
    )

    dataset_dir = os.path.join(os.path.dirname(__file__), "dataset")

    if input_mode == "Kaggle CUAD Dataset":
        sample_options = {
            "Service Agreement (ABC Tech & XYZ)": "sample_service_agreement.txt",
            "Service Agreement [PDF format]": "sample_service_agreement.pdf",
            "Mutual Non-Disclosure Agreement": "sample_nda.txt",
            "Software License & SaaS Agreement": "sample_software_license.txt",
        }
        selected_sample = st.selectbox("Select Kaggle Document:", list(sample_options.keys()))
        sample_path = os.path.join(dataset_dir, sample_options[selected_sample])

        if st.button("Load Selected Contract", type="primary", use_container_width=True):
            ext = "pdf" if sample_path.endswith(".pdf") else "txt"
            raw_text, meta = load_document(ext, sample_path)
            st.session_state.raw_text = raw_text
            st.session_state.metadata = meta
            st.session_state.preprocessed = preprocess_document(raw_text)
            st.session_state.analysis = None
            st.success(f"Loaded: {selected_sample}")

    elif input_mode == "Upload .txt / .pdf":
        uploaded_file = st.file_uploader("Upload contract file", type=["txt", "pdf"])
        if uploaded_file is not None:
            if st.button("Process Uploaded File", type="primary", use_container_width=True):
                temp_path = os.path.join(dataset_dir, f"temp_{uploaded_file.name}")
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())
                ext = "pdf" if uploaded_file.name.endswith(".pdf") else "txt"
                raw_text, meta = load_document(ext, temp_path)
                st.session_state.raw_text = raw_text
                st.session_state.metadata = meta
                st.session_state.preprocessed = preprocess_document(raw_text)
                st.session_state.analysis = None
                st.success("Uploaded file processed successfully!")

    else:
        text_input = st.text_area("Paste legal contract text here:", height=200)
        if st.button("Load Pasted Text", type="primary", use_container_width=True):
            if text_input.strip():
                raw_text, meta = load_document("keyboard", text_input)
                st.session_state.raw_text = raw_text
                st.session_state.metadata = meta
                st.session_state.preprocessed = preprocess_document(raw_text)
                st.session_state.analysis = None
                st.success("Custom legal text loaded!")

    st.markdown("---")
    st.markdown("#### ⚙️ Model Configuration")
    api_key_input = st.text_input("OpenAI API Key (Optional):", type="password")
    selected_model = st.selectbox("Model:", ["gpt-4o", "gpt-4-turbo", "gpt-4"], index=0)
    st.caption("If no API key is provided, the application runs via its intelligent local extraction engine.")


# Main Content Area
st.markdown('<div class="main-header">Automated Legal Document Analyzer</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Automated legal contract intelligence, clause extraction, and summarization with GPT-4</div>',
    unsafe_allow_html=True,
)

if not st.session_state.raw_text:
    # Auto-load default dataset if nothing loaded
    default_txt = os.path.join(dataset_dir, "sample_service_agreement.txt")
    if os.path.exists(default_txt):
        raw_text, meta = load_document("txt", default_txt)
        st.session_state.raw_text = raw_text
        st.session_state.metadata = meta
        st.session_state.preprocessed = preprocess_document(raw_text)

# Top Metrics Row
meta = st.session_state.metadata or {}
prep = st.session_state.preprocessed or {}
stats = prep.get("stats", {})

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Document Source", meta.get("source_type", "N/A").upper())
with col2:
    st.metric("Total Characters", f"{meta.get('char_count', 0):,}")
with col3:
    st.metric("Total Words", f"{meta.get('word_count', 0):,}")
with col4:
    st.metric("Sections Detected", stats.get("sections_found", 0))

st.markdown("---")

# Main Action Button: Analyze Document
c_btn1, c_btn2 = st.columns([2, 5])
with c_btn1:
    analyze_btn = st.button("🚀 Analyze Document with GPT-4", type="primary", use_container_width=True)

if analyze_btn or st.session_state.analysis:
    if analyze_btn:
        with st.spinner("Analyzing legal obligations, parties, payment terms, and clauses..."):
            analyzer = LegalDocumentAnalyzer(
                api_key=api_key_input.strip() if api_key_input else None,
                model=selected_model,
            )
            analysis = analyzer.analyze_document(st.session_state.preprocessed["cleaned_text"])
            st.session_state.analysis = analysis

    analysis = st.session_state.analysis

    st.markdown(f"**Analysis Engine:** `{analysis.get('mode')}`")

    # Tabs for structured viewing
    tab_summary, tab_clauses, tab_prep, tab_raw = st.tabs([
        "📋 Concise Summary (Q5)",
        "🔍 Structured Clause Breakdown",
        "⚙️ Preprocessing (Q3)",
        "📄 Raw Legal Document",
    ])

    with tab_summary:
        st.markdown("### Legal Document Summary (Part D - Q5)")
        st.markdown(f'<div class="summary-box">{analysis.get("summary")}</div>', unsafe_allow_html=True)

        st.markdown("---")
        # Save Report Section (Q6)
        c_save1, c_save2 = st.columns([3, 1])
        with c_save1:
            save_name = st.text_input("Output filename:", value="outputs/legal_analysis.txt")
        with c_save2:
            st.write("")
            st.write("")
            save_clicked = st.button("💾 Save Report (Q6)", use_container_width=True)
            if save_clicked:
                out_path = save_analysis_report(analysis["full_analysis"], save_name)
                st.success(f"Report saved to {out_path}")

        # Download button
        st.download_button(
            label="⬇️ Download Analysis (.txt)",
            data=analysis["full_analysis"],
            file_name="legal_analysis.txt",
            mime="text/plain",
        )

    with tab_clauses:
        st.markdown("### Full Legal Clause Analysis")
        st.text_area("Complete Output", analysis["full_analysis"], height=450)

    with tab_prep:
        st.markdown("### Document Preprocessing Details (Part B - Q3)")
        pcol1, pcol2 = st.columns(2)
        with pcol1:
            st.markdown("#### Preprocessing Operations:")
            st.markdown("- ✅ Removed unnecessary whitespaces & redundant line breaks")
            st.markdown("- ✅ Removed non-printable & control characters")
            st.markdown("- ✅ Normalized smart quotes, hyphens, and bullet points")
            st.markdown(f"- ✅ Original length: `{stats.get('original_length')} characters`")
            st.markdown(f"- ✅ Cleaned length: `{stats.get('cleaned_length')} characters`")
            st.markdown(f"- ✅ Cleaned text reduction: `{stats.get('characters_removed')} characters`")

        with pcol2:
            st.markdown("#### Detected Sections:")
            sections = prep.get("sections", [])
            if sections:
                for s in sections:
                    st.markdown(f"- **{s['heading']}**")
            else:
                st.caption("No explicit numbered section headers identified.")

    with tab_raw:
        st.markdown("### Raw Extracted Text")
        st.text_area("Document Content", st.session_state.raw_text, height=400)

else:
    st.info("Click **'🚀 Analyze Document with GPT-4'** above to run the legal clause analysis and generate summary.")
    with st.expander("Preview Loaded Document", expanded=True):
        st.text_area("Document Text", st.session_state.raw_text or "", height=350)
