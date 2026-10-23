"""
Module: file_handler.py
Part A (Q1, Q2) - Legal Document Input & Display
Part E (Q6)     - Save Analysis Report
"""

import os
from typing import Dict, Any, Tuple


def read_text_file(filepath: str) -> str:
    """
    Read legal document from a .txt file with automatic encoding fallback.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    encodings = ["utf-8", "utf-8-sig", "latin-1", "cp1252"]
    for enc in encodings:
        try:
            with open(filepath, "r", encoding=enc) as f:
                content = f.read()
                return content
        except UnicodeDecodeError:
            continue

    raise ValueError(f"Unable to decode text file with standard encodings: {filepath}")


def read_pdf_file(filepath: str) -> str:
    """
    Extract text content from a .pdf legal document using pypdf.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"PDF file not found: {filepath}")

    try:
        from pypdf import PdfReader
    except ImportError:
        raise ImportError("pypdf is required for PDF reading. Install via `pip install pypdf`.")

    reader = PdfReader(filepath)
    extracted_text = []

    for idx, page in enumerate(reader.pages):
        page_text = page.extract_text()
        if page_text:
            extracted_text.append(f"--- [Page {idx + 1}] ---\n{page_text}")

    full_text = "\n\n".join(extracted_text).strip()
    if not full_text:
        raise ValueError(f"No readable text could be extracted from PDF: {filepath}")

    return full_text


def load_document(source_type: str, source_val: str) -> Tuple[str, Dict[str, Any]]:
    """
    Q1: Read a legal document from user through keyboard input, .txt file, or .pdf file.
    
    Returns:
        tuple: (raw_text, metadata_dict)
    """
    source_type = source_type.lower().strip()
    metadata: Dict[str, Any] = {
        "source_type": source_type,
        "source_path": source_val if source_type in ["txt", "pdf"] else "Direct Keyboard Input",
    }

    if source_type == "keyboard":
        raw_text = source_val.strip()
    elif source_type == "txt":
        raw_text = read_text_file(source_val)
    elif source_type == "pdf":
        raw_text = read_pdf_file(source_val)
    else:
        raise ValueError(f"Unsupported source type: {source_type}. Supported: 'keyboard', 'txt', 'pdf'")

    # Extract provisional title
    lines = [line.strip() for line in raw_text.splitlines() if line.strip()]
    metadata["detected_title"] = lines[0] if lines else "Untitled Legal Document"
    metadata["char_count"] = len(raw_text)
    metadata["word_count"] = len(raw_text.split())
    metadata["line_count"] = len(raw_text.splitlines())

    return raw_text, metadata


def display_document_info(raw_text: str, metadata: Dict[str, Any], preview_chars: int = 400) -> str:
    """
    Q2: Display the document information neatly.
    """
    title = metadata.get("detected_title", "Untitled Legal Document")
    src_type = metadata.get("source_type", "Unknown").upper()
    src_path = metadata.get("source_path", "N/A")
    words = metadata.get("word_count", len(raw_text.split()))
    chars = metadata.get("char_count", len(raw_text))
    est_reading_time = max(1, round(words / 200))  # Standard 200 WPM

    border = "=" * 65
    info = [
        border,
        "                   DOCUMENT INFORMATION",
        border,
        f"  Title / Heading   : {title}",
        f"  Input Source      : {src_type} ({src_path})",
        f"  Total Characters  : {chars:,}",
        f"  Total Words       : {words:,}",
        f"  Est. Reading Time : ~{est_reading_time} minute(s)",
        border,
        "  Document Preview (First 400 characters):",
        "  " + "-" * 61,
        "  " + "\n  ".join(raw_text[:preview_chars].splitlines()[:10]),
        "  ...",
        border,
    ]
    formatted_output = "\n".join(info)
    return formatted_output


def save_analysis_report(content: str, output_path: str = "outputs/legal_analysis.txt") -> str:
    """
    Q6: Save the generated analysis to a file.
    Creates parent directories if necessary.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    return os.path.abspath(output_path)
