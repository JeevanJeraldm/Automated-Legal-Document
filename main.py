"""
================================================================================
EXPERIMENT 5: AUTOMATED LEGAL DOCUMENT ANALYZER USING GPT-4
================================================================================
Part F (Q7): Complete Integrated Application
CLI Interface matching options:
1. Upload / Enter Legal Document
2. Analyze Document
3. Generate Summary
4. Save Report
5. Exit
================================================================================
"""

import sys
import os

# Add local directory to path
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from src.file_handler import load_document, display_document_info, save_analysis_report
from src.preprocessor import preprocess_document
from src.prompt_builder import build_analysis_prompt
from src.analyzer import LegalDocumentAnalyzer


def print_banner():
    banner = """
======================================================================
       EXPERIMENT 5: AUTOMATED LEGAL DOCUMENT ANALYZER (GPT-4)
======================================================================
  Domain: Legal Contract Intelligence & Clause Extraction
  Model : OpenAI GPT-4 / Intelligent Fallback Engine
  Data  : Kaggle CUAD (Contract Understanding Atticus Dataset)
======================================================================
"""
    print(banner)


def display_menu():
    print("\n" + "=" * 50)
    print("                 MAIN MENU")
    print("=" * 50)
    print("  1. Upload / Enter Legal Document")
    print("  2. Analyze Document")
    print("  3. Generate Summary")
    print("  4. Save Report")
    print("  5. Exit")
    print("=" * 50)


def choose_sample_dataset() -> str:
    dataset_dir = os.path.join(os.path.dirname(__file__), "dataset")
    samples = [
        ("sample_service_agreement.txt", "Service Agreement (ABC Tech & XYZ Solutions) [Recommended]"),
        ("sample_service_agreement.pdf", "Service Agreement in PDF format (Tests PDF text extraction)"),
        ("sample_nda.txt", "Mutual Non-Disclosure Agreement (Apex & Quantum)"),
        ("sample_software_license.txt", "Enterprise Software License & SaaS Agreement"),
    ]

    print("\nSelect a sample document from Kaggle CUAD dataset:")
    for idx, (fname, desc) in enumerate(samples, 1):
        print(f"  [{idx}] {desc} ({fname})")

    choice = input("\nEnter choice [1-4] (default 1): ").strip()
    if not choice or choice not in ["1", "2", "3", "4"]:
        choice = "1"

    selected_file = samples[int(choice) - 1][0]
    return os.path.join(dataset_dir, selected_file)


def handle_input_document() -> tuple:
    print("\n--- Part A (Q1): Read Legal Document ---")
    print("Choose input method:")
    print("  [1] Select from Kaggle CUAD Dataset (.txt / .pdf)")
    print("  [2] Load a custom .txt file")
    print("  [3] Load a custom .pdf file")
    print("  [4] Enter / paste legal text directly via keyboard")

    choice = input("Enter choice [1-4] (default 1): ").strip() or "1"

    if choice == "1":
        filepath = choose_sample_dataset()
        ext = "pdf" if filepath.endswith(".pdf") else "txt"
        raw_text, meta = load_document(ext, filepath)
    elif choice == "2":
        filepath = input("Enter path to .txt file: ").strip()
        raw_text, meta = load_document("txt", filepath)
    elif choice == "3":
        filepath = input("Enter path to .pdf file: ").strip()
        raw_text, meta = load_document("pdf", filepath)
    elif choice == "4":
        print("\nEnter legal text below (type 'END' on a new line when finished):")
        lines = []
        while True:
            line = input()
            if line.strip() == "END":
                break
            lines.append(line)
        raw_text = "\n".join(lines)
        raw_text, meta = load_document("keyboard", raw_text)
    else:
        print("Invalid choice, defaulting to Kaggle sample Service Agreement.")
        filepath = os.path.join(os.path.dirname(__file__), "dataset", "sample_service_agreement.txt")
        raw_text, meta = load_document("txt", filepath)

    # Part A - Q2: Display document information neatly
    print("\n--- Part A (Q2): Document Information ---")
    doc_info = display_document_info(raw_text, meta)
    print(doc_info)

    # Part B - Q3: Document Preprocessing
    print("\n--- Part B (Q3): Document Preprocessing ---")
    preprocessed = preprocess_document(raw_text)
    print(f"  [+] Unwanted characters removed")
    print(f"  [+] Redundant spaces normalized")
    print(f"  [+] Original length : {preprocessed['stats']['original_length']} chars")
    print(f"  [+] Cleaned length  : {preprocessed['stats']['cleaned_length']} chars")
    print(f"  [+] Sections found  : {preprocessed['stats']['sections_found']}")
    if preprocessed["sections"]:
        print("      Detected Sections:")
        for sec in preprocessed["sections"][:6]:
            print(f"        - {sec['heading']}")
    print(f"  [+] Document chunks : {preprocessed['stats']['chunks_created']}")

    return raw_text, meta, preprocessed


def main():
    print_banner()

    analyzer = LegalDocumentAnalyzer()
    print(f"[*] Engine Status: {'OpenAI GPT-4 Ready' if analyzer.is_api_configured() else 'Resilient Offline Analysis Mode Active'}")
    if not analyzer.is_api_configured():
        print("    (Tip: Set OPENAI_API_KEY in .env to use live OpenAI GPT-4 API)")

    raw_text = None
    meta = None
    preprocessed = None
    analysis_results = None
    summary_output = None

    while True:
        display_menu()
        choice = input("Enter your choice (1-5): ").strip()

        if choice == "1":
            try:
                raw_text, meta, preprocessed = handle_input_document()
                # Reset downstream state for new document
                analysis_results = None
                summary_output = None
            except Exception as e:
                print(f"\n[!] Error loading document: {e}")

        elif choice == "2":
            if not preprocessed:
                print("\n[!] Please upload or enter a legal document first (Option 1).")
                continue

            print("\n--- Part C (Q4) & Part D (Q5): Analyzing Document with GPT-4 ---")
            print("[*] Generating GPT-4 prompt with strict zero-hallucination constraint...")
            sample_prompt = build_analysis_prompt(preprocessed["cleaned_text"])
            print(f"[*] Prompt constructed successfully ({len(sample_prompt)} characters).")
            print("[*] Analyzing document content, obligations, payment, and clauses...")

            try:
                analysis_results = analyzer.analyze_document(preprocessed["cleaned_text"])
                summary_output = analysis_results.get("summary")
                print(f"\n[+] Analysis Complete! [Engine: {analysis_results.get('mode')}]")
                if "engine_notice" in analysis_results:
                    print(f"    Note: {analysis_results['engine_notice']}")

                print("\n" + "=" * 65)
                print(analysis_results["full_analysis"])
                print("=" * 65)
            except Exception as e:
                print(f"\n[!] Analysis failed: {e}")

        elif choice == "3":
            if not preprocessed:
                print("\n[!] Please upload or enter a legal document first (Option 1).")
                continue

            print("\n--- Part D (Q5): Concise Legal Document Summary ---")
            if not summary_output:
                print("[*] Generating concise summary block...")
                summary_output = analyzer.generate_summary(preprocessed["cleaned_text"])

            print("\n" + "=" * 50)
            print(summary_output)
            print("=" * 50)

        elif choice == "4":
            if not analysis_results and not summary_output:
                print("\n[!] Please analyze the document (Option 2) or generate summary (Option 3) first.")
                continue

            print("\n--- Part E (Q6): Save Analysis Report ---")
            report_text = analysis_results["full_analysis"] if analysis_results else summary_output
            default_path = os.path.join(os.path.dirname(__file__), "outputs", "legal_analysis.txt")
            custom_path = input(f"Enter output path [default: outputs/legal_analysis.txt]: ").strip()
            save_path = custom_path if custom_path else default_path

            try:
                saved_file = save_analysis_report(report_text, save_path)
                print(f"[+] Report successfully saved to:\n    {saved_file}")
                print(f"[+] File Size: {os.path.getsize(saved_file)} bytes")
            except Exception as e:
                print(f"[!] Error saving report: {e}")

        elif choice == "5":
            print("\nExiting Automated Legal Document Analyzer. Goodbye!")
            sys.exit(0)

        else:
            print("\n[!] Invalid selection. Please enter a number between 1 and 5.")


if __name__ == "__main__":
    main()
