"""
Module: preprocessor.py
Part B (Q3) - Document Preprocessing:
- Remove unnecessary spaces
- Remove unwanted characters
- Normalize text
- Identify sections
- Divide long documents into chunks where necessary
"""

import re
from typing import List, Dict, Any, Tuple


def remove_unnecessary_spaces(text: str) -> str:
    """
    Remove redundant whitespaces, multiple spaces, tabs, and excess newlines.
    """
    # Replace horizontal tabs and non-breaking spaces with standard space
    text = re.sub(r"[ \t\u00a0]+", " ", text)
    # Strip whitespace from each line
    lines = [line.strip() for line in text.splitlines()]
    # Collapse 3 or more blank lines into a double newline
    cleaned_text = "\n".join(lines)
    cleaned_text = re.sub(r"\n{3,}", "\n\n", cleaned_text)
    return cleaned_text.strip()


def remove_unwanted_characters(text: str) -> str:
    """
    Remove non-printable characters, zero-width spaces, and control artifacts.
    Preserves normal text, newlines, and standard legal punctuation.
    """
    # Remove BOM and zero-width spaces
    text = text.replace("\ufeff", "").replace("\u200b", "").replace("\r", "")
    # Remove control characters except tab and newline
    text = re.sub(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", "", text)
    return text


def normalize_text(text: str) -> str:
    """
    Normalize punctuation, quotes, dashes, and standard legal formatting.
    """
    # Smart quotes to standard quotes
    text = text.replace("“", '"').replace("”", '"').replace("„", '"')
    text = text.replace("‘", "'").replace("’", "'").replace("`", "'")

    # En-dash, Em-dash, minus to standard hyphen
    text = text.replace("—", " - ").replace("–", " - ").replace("−", "-")

    # Standardize bullet symbols
    text = re.sub(r"^[•*▪►]\s*", "- ", text, flags=re.MULTILINE)

    return text


def identify_sections(text: str) -> List[Dict[str, Any]]:
    """
    Identify standard legal contract sections and headings.
    Recognizes formats like:
      - '1. PURPOSE'
      - 'SECTION 2 - PAYMENT TERMS'
      - 'ARTICLE III: TERMINATION'
      - All-caps section headers
    """
    section_patterns = [
        # Numbered headings: 1. PURPOSE or 1.1 Scope
        r"(?m)^(?:\d+\.|\d+\.\d+|\([a-z0-9]+\))\s+([A-Z][A-Za-z0-9 ,/&\-]{3,60})$",
        # Section / Article: SECTION 1: DEFINITIONS
        r"(?m)^(?:SECTION|ARTICLE|CLAUSE)\s+[0-9IVXLCDM]+[:\.\-]?\s*([A-Za-z0-9 ,/&\-]{3,60})$",
        # Standalone uppercase heading lines
        r"(?m)^([A-Z0-9][A-Z0-9 ,/&\-]{4,50})$",
    ]

    detected_sections = []
    seen_titles = set()

    for pattern in section_patterns:
        for match in re.finditer(pattern, text):
            full_match = match.group(0).strip()
            # Filter out short false positives or common phrases that aren't headings
            if len(full_match) < 4 or full_match in seen_titles:
                continue
            if full_match.lower().startswith(("in witness", "by:", "name:", "title:", "page ")):
                continue

            seen_titles.add(full_match)
            detected_sections.append({
                "heading": full_match,
                "start_char": match.start(),
                "end_char": match.end(),
            })

    # Sort sections by occurrence in document
    detected_sections.sort(key=lambda s: s["start_char"])
    return detected_sections


def divide_into_chunks(text: str, max_chunk_size: int = 3000, overlap: int = 300) -> List[str]:
    """
    Divide long legal documents into overlapping chunks where necessary.
    Preserves context across chunk boundaries.
    """
    if len(text) <= max_chunk_size:
        return [text]

    chunks = []
    paragraphs = text.split("\n\n")
    current_chunk = []
    current_length = 0

    for para in paragraphs:
        para_len = len(para)
        if current_length + para_len + 2 > max_chunk_size and current_chunk:
            chunk_text = "\n\n".join(current_chunk)
            chunks.append(chunk_text)

            # Keep tail for overlap context
            overlap_text = chunk_text[-overlap:] if len(chunk_text) > overlap else ""
            current_chunk = [overlap_text, para] if overlap_text else [para]
            current_length = len(overlap_text) + para_len
        else:
            current_chunk.append(para)
            current_length += para_len + 2

    if current_chunk:
        chunks.append("\n\n".join(current_chunk))

    return chunks


def preprocess_document(raw_text: str) -> Dict[str, Any]:
    """
    Orchestrate full preprocessing pipeline:
    1. Unwanted character removal
    2. Text normalization
    3. Unnecessary space removal
    4. Section identification
    5. Document chunking
    """
    step1 = remove_unwanted_characters(raw_text)
    step2 = normalize_text(step1)
    cleaned_text = remove_unnecessary_spaces(step2)

    sections = identify_sections(cleaned_text)
    chunks = divide_into_chunks(cleaned_text)

    stats = {
        "original_length": len(raw_text),
        "cleaned_length": len(cleaned_text),
        "characters_removed": len(raw_text) - len(cleaned_text),
        "sections_found": len(sections),
        "chunks_created": len(chunks),
    }

    return {
        "cleaned_text": cleaned_text,
        "sections": sections,
        "chunks": chunks,
        "stats": stats,
    }
