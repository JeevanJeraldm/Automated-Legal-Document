"""
Module: prompt_builder.py
Part C (Q4) - Prompt Generation:
Constructs a GPT-4 prompt instructing the model to analyze the legal document.
Requests:
- Summary
- Parties
- Purpose
- Obligations
- Payment terms
- Duration
- Termination conditions
- Important dates
- Key clauses

Constraint:
"Do not invent information. If information is not available, state 'Not mentioned in the document.'"
"""


def build_system_prompt() -> str:
    """
    Constructs the system prompt establishing the GPT-4 legal analyst persona.
    """
    return (
        "You are an expert Automated Legal Document Analyst specializing in corporate "
        "contracts, commercial agreements, and legal text summarization. Your task is to perform "
        "a rigorous, factual analysis of legal documents. You must adhere strictly to the text provided.\n\n"
        "CRITICAL CONSTRAINT:\n"
        "Do not invent information. If information is not available, state 'Not mentioned in the document.'"
    )


def build_analysis_prompt(document_text: str) -> str:
    """
    Q4: Construct a GPT-4 prompt that instructs the model to analyze the legal document.
    """
    prompt = f"""You are provided with a legal document below. Analyze its content thoroughly and extract the required legal elements in the exact structured format shown.

=== INSTRUCTIONS & CONSTRAINTS ===
1. Analyze the legal text objectively and accurately.
2. Do not invent information. If information is not available, state "Not mentioned in the document."
3. First, provide the concise standardized summary block matching the format:
   LEGAL DOCUMENT SUMMARY
   --------------------------------
   Document Type:
   <Document Type>
   Parties:
   <Parties>
   Purpose:
   <Purpose>
   Duration:
   <Duration>
   Summary:
   <Concise summary of the agreement>

4. Next, provide the detailed breakdown covering every one of the following items:
   - Summary: Detailed overview of the legal contract
   - Parties: Full legal names, roles, and addresses of all contracting parties
   - Purpose: Main objective and scope of the agreement
   - Obligations: Specific obligations, deliverables, and responsibilities of each party
   - Payment terms: Compensation, invoicing frequency, payment window, penalties/interest
   - Duration: Effective date, term length, expiration or renewal provisions
   - Termination conditions: Grounds for termination (convenience, cause, insolvency, notice period)
   - Important dates: Effective date, milestone dates, renewal dates, expiration dates
   - Key clauses: Confidentiality, intellectual property, governing law, dispute resolution, liability limits

=== LEGAL DOCUMENT TEXT ===
{document_text}

=== BEGIN ANALYSIS ===
"""
    return prompt.strip()


def build_summary_only_prompt(document_text: str) -> str:
    """
    Constructs a targeted prompt requesting only the concise legal summary block
    matching the exact sample output format from Q5.
    """
    prompt = f"""You are an expert legal document analyst. Based ONLY on the legal document text provided below, generate the concise legal summary in this EXACT structure:

LEGAL DOCUMENT SUMMARY
--------------------------------
Document Type:
<Document Type>
Parties:
<Parties>
Purpose:
<Purpose>
Duration:
<Duration>
Summary:
<Concise paragraph summarizing the agreement, responsibilities, payment, confidentiality, and termination>

STRICT RULE: Do not invent information. If information is not available, state "Not mentioned in the document."

=== LEGAL DOCUMENT TEXT ===
{document_text}
"""
    return prompt.strip()
