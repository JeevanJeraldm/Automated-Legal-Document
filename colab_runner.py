# ============================================================
# Google Colab Runner: Experiment 5
# Automated Legal Document Analyzer using GPT-4
# ============================================================
# Copy this file to a Google Colab notebook cell-by-cell
# or run directly in shell: python colab_runner.py
# ============================================================

# ── CELL 1: Install Dependencies ────────────────────────────
import subprocess
import sys
import os

packages = [
    "openai>=1.0.0",
    "pypdf>=3.0.0",
    "python-dotenv>=1.0.0",
    "reportlab>=3.6.0",
    "streamlit>=1.20.0"
]

print("[*] Installing required packages...")
for pkg in packages:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", pkg])
print("[+] Dependencies installed successfully!\n")

# ── CELL 2: Setup Workspace & Imports ───────────────────────
from src.file_handler import load_document, display_document_info, save_analysis_report
from src.preprocessor import preprocess_document
from src.prompt_builder import build_analysis_prompt, build_system_prompt
from src.analyzer import LegalDocumentAnalyzer

print("[+] Modules imported successfully!")

# ── CELL 3: Part A - Legal Document Input & Display ─────────
print("\n" + "="*60)
print("PART A: LEGAL DOCUMENT INPUT & DISPLAY (Q1 & Q2)")
print("="*60)

sample_file = os.path.join("dataset", "sample_service_agreement.txt")
raw_text, meta = load_document("txt", sample_file)
doc_info = display_document_info(raw_text, meta)
print(doc_info)

# Also demonstrate PDF extraction
pdf_sample = os.path.join("dataset", "sample_service_agreement.pdf")
if os.path.exists(pdf_sample):
    pdf_text, pdf_meta = load_document("pdf", pdf_sample)
    print("\n[+] PDF Extraction Verified Successfully!")
    print(f"    Extracted {pdf_meta['char_count']} characters from PDF.")

# ── CELL 4: Part B - Document Preprocessing ─────────────────
print("\n" + "="*60)
print("PART B: DOCUMENT PREPROCESSING (Q3)")
print("="*60)

prep = preprocess_document(raw_text)
stats = prep["stats"]
print(f"Original Character Count: {stats['original_length']}")
print(f"Cleaned Character Count : {stats['cleaned_length']}")
print(f"Characters Filtered     : {stats['characters_removed']}")
print(f"Sections Identified     : {stats['sections_found']}")
for idx, sec in enumerate(prep["sections"], 1):
    print(f"  {idx}. {sec['heading']}")
print(f"Chunks Formed           : {stats['chunks_created']}")

# ── CELL 5: Part C - Prompt Generation ──────────────────────
print("\n" + "="*60)
print("PART C: GPT-4 PROMPT GENERATION (Q4)")
print("="*60)

system_prompt = build_system_prompt()
user_prompt = build_analysis_prompt(prep["cleaned_text"][:800] + "\n...[truncated for display]...")
print("System Prompt:")
print("-" * 40)
print(system_prompt)
print("\nConstructed User Prompt Preview:")
print("-" * 40)
print(user_prompt[:600] + "\n...\n[END PROMPT PREVIEW]")

# ── CELL 6: Part D - Summarization & Legal Analysis ─────────
print("\n" + "="*60)
print("PART D: LEGAL DOCUMENT SUMMARIZATION & CLAUSE EXTRACTION (Q5)")
print("="*60)

analyzer = LegalDocumentAnalyzer()
analysis_result = analyzer.analyze_document(prep["cleaned_text"])
print(f"Engine Used: {analysis_result['mode']}\n")
print(analysis_result["summary"])

# ── CELL 7: Part E - Save Analysis Report ───────────────────
print("\n" + "="*60)
print("PART E: SAVE ANALYSIS REPORT (Q6)")
print("="*60)

output_file = os.path.join("outputs", "legal_analysis.txt")
saved_path = save_analysis_report(analysis_result["full_analysis"], output_file)
print(f"[+] Full legal analysis successfully saved to: {saved_path}")
print(f"[+] Output File Size: {os.path.getsize(saved_path)} bytes")

# ── CELL 8: Summary Verification ────────────────────────────
print("\n" + "="*60)
print("EXPERIMENT 5 EXECUTION VERIFICATION: ALL MODULES PASSED!")
print("="*60)
