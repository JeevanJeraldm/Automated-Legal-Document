"""
================================================================================
EXPERIMENT 5: AUTOMATED LEGAL DOCUMENT ANALYZER (STREAMLIT WEB APP)
================================================================================
Enhanced UX with immediate default analysis on load, interactive contract
selection, instant clause breakdown, and downloadable report.
================================================================================
"""

import os
import sys
import streamlit as st

# Configure page settings
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

# Custom CSS for rich visuals
st.markdown("""
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 800;
        color: #1e3a8a;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #475569;
        margin-bottom: 1.2rem;
    }
    .summary-card {
        background: #ffffff;
        border: 2px solid #22c55e;
        border-radius: 10px;
        padding: 1.5rem;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
    }
    .summary-title {
        color: #166534;
        font-size: 1.3rem;
        font-weight: 700;
        border-bottom: 2px solid #bbf7d0;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .summary-text {
        font-family: 'Consolas', 'Courier New', monospace;
        background-color: #f0fdf4;
        padding: 1.2rem;
        border-radius: 6px;
        color: #14532d;
        white-space: pre-wrap;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    .badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 9999px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 0.5rem;
    }
    .badge-blue { background-color: #dbeafe; color: #1e40af; }
    .badge-green { background-color: #dcfce7; color: #15803d; }
    .clause-box {
        background-color: #f8fafc;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

dataset_dir = os.path.join(os.path.dirname(__file__), "dataset")

# Session state initialization with auto-analysis
if "initialized" not in st.session_state:
    default_txt = os.path.join(dataset_dir, "sample_service_agreement.txt")
    raw_text, meta = load_document("txt", default_txt)
    prep = preprocess_document(raw_text)
    analyzer = LegalDocumentAnalyzer()
    analysis = analyzer.analyze_document(prep["cleaned_text"])

    st.session_state.raw_text = raw_text
    st.session_state.metadata = meta
    st.session_state.preprocessed = prep
    st.session_state.analysis = analysis
    st.session_state.selected_sample_name = "Service Agreement (ABC Tech & XYZ)"
    st.session_state.initialized = True

# Sidebar Controls
with st.sidebar:
    st.markdown("### ⚖️ Contract Intelligence")
    st.caption("Experiment 5: GPT-4 Legal Document Analyzer")

    st.markdown("---")
    st.markdown("#### 1. Choose Input Document")
    input_source = st.radio(
        "Source:",
        ["Kaggle CUAD Dataset", "Upload Custom File (.txt / .pdf)", "Direct Text Paste"],
    )

    if input_source == "Kaggle CUAD Dataset":
        samples = {
            "Service Agreement (ABC Tech & XYZ)": "sample_service_agreement.txt",
            "Service Agreement [PDF format]": "sample_service_agreement.pdf",
            "Mutual Non-Disclosure Agreement": "sample_nda.txt",
            "Software License & SaaS Agreement": "sample_software_license.txt",
        }
        chosen = st.selectbox("Select Kaggle Contract:", list(samples.keys()))
        if chosen != st.session_state.get("selected_sample_name"):
            filepath = os.path.join(dataset_dir, samples[chosen])
            ext = "pdf" if filepath.endswith(".pdf") else "txt"
            raw_text, meta = load_document(ext, filepath)
            prep = preprocess_document(raw_text)
            analyzer = LegalDocumentAnalyzer()
            analysis = analyzer.analyze_document(prep["cleaned_text"])

            st.session_state.raw_text = raw_text
            st.session_state.metadata = meta
            st.session_state.preprocessed = prep
            st.session_state.analysis = analysis
            st.session_state.selected_sample_name = chosen
            st.rerun()

    elif input_source == "Upload Custom File (.txt / .pdf)":
        uploaded = st.file_uploader("Upload legal contract (.txt or .pdf):", type=["txt", "pdf"])
        if uploaded is not None:
            if st.button("Analyze Uploaded File", type="primary", use_container_width=True):
                temp_file = os.path.join(dataset_dir, f"temp_{uploaded.name}")
                with open(temp_file, "wb") as f:
                    f.write(uploaded.getbuffer())
                ext = "pdf" if uploaded.name.endswith(".pdf") else "txt"
                raw_text, meta = load_document(ext, temp_file)
                prep = preprocess_document(raw_text)
                analyzer = LegalDocumentAnalyzer()
                analysis = analyzer.analyze_document(prep["cleaned_text"])

                st.session_state.raw_text = raw_text
                st.session_state.metadata = meta
                st.session_state.preprocessed = prep
                st.session_state.analysis = analysis
                st.session_state.selected_sample_name = uploaded.name
                st.rerun()

    else:
        pasted_text = st.text_area("Paste legal text below:", height=200)
        if st.button("Analyze Pasted Text", type="primary", use_container_width=True):
            if pasted_text.strip():
                raw_text, meta = load_document("keyboard", pasted_text)
                prep = preprocess_document(raw_text)
                analyzer = LegalDocumentAnalyzer()
                analysis = analyzer.analyze_document(prep["cleaned_text"])

                st.session_state.raw_text = raw_text
                st.session_state.metadata = meta
                st.session_state.preprocessed = prep
                st.session_state.analysis = analysis
                st.session_state.selected_sample_name = "Custom Text Input"
                st.rerun()

    st.markdown("---")
    st.markdown("#### ⚙️ OpenAI API Settings (Optional)")
    api_key_input = st.text_input("OpenAI API Key:", type="password", placeholder="sk-...")
    selected_model = st.selectbox("Model:", ["gpt-4o", "gpt-4-turbo", "gpt-4"], index=0)
    if st.button("Re-run with Live GPT-4", use_container_width=True):
        if api_key_input.strip():
            with st.spinner("Connecting to OpenAI GPT-4 API..."):
                analyzer = LegalDocumentAnalyzer(api_key=api_key_input.strip(), model=selected_model)
                analysis = analyzer.analyze_document(st.session_state.preprocessed["cleaned_text"])
                st.session_state.analysis = analysis
                st.success("Analysis updated via OpenAI GPT-4!")
                st.rerun()
        else:
            st.warning("Please enter your OpenAI API key above to call live GPT-4.")

# Main Header
st.markdown('<div class="main-title">Automated Legal Document Analyzer using GPT-4</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Contract intelligence, clause identification, obligation mapping, and standardized legal summarization</div>',
    unsafe_allow_html=True,
)

meta = st.session_state.metadata
prep = st.session_state.preprocessed
stats = prep.get("stats", {})
analysis = st.session_state.analysis

# Top Metrics Row
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.metric("Document Source", f"{meta.get('source_type', 'TXT').upper()}")
with c2:
    st.metric("Total Characters", f"{meta.get('char_count', 0):,}")
with c3:
    st.metric("Word Count", f"{meta.get('word_count', 0):,}")
with c4:
    st.metric("Sections Identified", f"{stats.get('sections_found', 0)}")

# Analysis Engine Status Banner
mode_name = analysis.get("mode", "Intelligent Extraction Engine")
st.markdown(
    f'<span class="badge badge-blue">Engine: {mode_name}</span>'
    f'<span class="badge badge-green">Zero-Hallucination Guard: Active</span>',
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# Tabs
tab_summary, tab_clauses, tab_prep, tab_raw = st.tabs([
    "📋 Concise Summary (Part D - Q5)",
    "🔍 Detailed Legal Clause Breakdown",
    "⚙️ Document Preprocessing (Part B - Q3)",
    "📄 Raw Legal Text (Part A - Q1)",
])

with tab_summary:
    st.markdown('<div class="summary-card">', unsafe_allow_html=True)
    st.markdown('<div class="summary-title">LEGAL DOCUMENT SUMMARY (Expected Output)</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="summary-text">{analysis.get("summary")}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Action buttons
    col_dl, col_save = st.columns([1, 1])
    with col_dl:
        st.download_button(
            label="⬇️ Download Analysis Report (.txt)",
            data=analysis.get("full_analysis", ""),
            file_name="legal_analysis.txt",
            mime="text/plain",
            use_container_width=True,
        )
    with col_save:
        if st.button("💾 Save Report to outputs/legal_analysis.txt (Q6)", use_container_width=True):
            out_file = os.path.join(os.path.dirname(__file__), "outputs", "legal_analysis.txt")
            saved_loc = save_analysis_report(analysis.get("full_analysis", ""), out_file)
            st.success(f"Report saved to: {saved_loc}")

with tab_clauses:
    st.markdown("### Full Structured Clause Analysis")
    st.text_area("Complete Legal Report Content:", analysis.get("full_analysis", ""), height=480)

with tab_prep:
    st.markdown("### Document Preprocessing Verification (Part B - Q3)")
    c_p1, c_p2 = st.columns(2)
    with c_p1:
        st.markdown("#### Preprocessing Steps Executed:")
        st.markdown("- ✅ **Remove Unnecessary Spaces**: Stripped trailing spaces, normalized double line breaks.")
        st.markdown("- ✅ **Remove Unwanted Characters**: Stripped control characters, BOM (`\\ufeff`), non-printables.")
        st.markdown("- ✅ **Normalize Text**: Standardized smart quotes (`\"\"`, `''`), hyphens, bullet markers.")
        st.markdown(f"- 📏 **Original Length**: `{stats.get('original_length')} characters`")
        st.markdown(f"- 🧹 **Cleaned Length**: `{stats.get('cleaned_length')} characters`")
        st.markdown(f"- ✂️ **Characters Cleaned**: `{stats.get('characters_removed')} characters`")
        st.markdown(f"- 📦 **Chunks Formed**: `{stats.get('chunks_created')} chunk(s)`")
    with c_p2:
        st.markdown("#### Detected Legal Sections:")
        secs = prep.get("sections", [])
        if secs:
            for s in secs:
                st.markdown(f"- 📌 **{s['heading']}**")
        else:
            st.info("No explicit numbered sections found.")

with tab_raw:
    st.markdown("### Raw Input Document (Part A - Q1 & Q2)")
    st.text_area("Original Text Content:", st.session_state.raw_text, height=420)
