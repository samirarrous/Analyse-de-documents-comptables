"""
Common extraction logic and regular expressions shared across different document types.
"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def extract_document_type(text):
    """
    Identifies the type of accounting document from its text content.

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The document type (e.g., 'liasse_fiscale', 'bilan'), or 'unknown'.
    """
    patterns = {
        "liasse_fiscale":  r"\bliasse\b",
        "compte_resultat": r"compte\s+de\s+r[eé]sultat",
        "bilan":           r"\bbilan\b",
        "facture":         r"\bfacture\b",
    }
    for doc_type, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE):
            return doc_type
    return "unknown"

def extract_date(text):
    """
    Extracts a date in the format DD/MM/YYYY or DD-MM-YYYY from the text.

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The extracted date, or 'unknown'.
    """
    pattern = r"\d{2}\s*[/-]\s*\d{2}\s*[/-]\s*\d{4}"
    match = re.search(pattern, text)
    if match:
        return match.group()
    return "unknown"

""" the company name is often before the juridical form, but not always, 
so i noticed that it's either the document type or the company name that is on the first line,

so i decided to check if the first line contains the document type,
if it does, then we will search for the company name in the rest of the text,
 otherwise we will consider that the first line as the company name
 """

def extract_company_name(text):
    """
    Extracts the company name from the document text.

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The extracted company name, or 'unknown'.
    """
    pattern = r"(?:DE\s*:\s*)?([A-ZÀ-ÿ0-9\s'&-]+?)\s+(?:EURL|SARL|SAS|SA|SCI|EI)"
    lines = text.split("\n")
    first_line = lines[0].strip()

    if extract_document_type(first_line) != "unknown":
        for line in lines[1:]:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                return match.group(1).strip()
    else:
        match = re.search(pattern, first_line, re.IGNORECASE)
        if match:
            return match.group(1).strip()
        return first_line
    return "unknown"

def extract_juridical_form(text):
    """
    Extracts the juridical form (legal entity type) of the company.

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The juridical form (e.g., 'SAS', 'SARL'), or 'unknown'.
    """
    pattern = r"\b(EURL|SARL|SAS|SA|SCI|EI)\b"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).upper()  
    return "unknown"

def extract_fiscal_year_end_date(text):
    """
    Extracts the closing date of the fiscal year.

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The closing date, or 'unknown'.
    """
    pattern1 = r"exercice\s+(?::\s*)?(\d{4})"
    match = re.search(pattern1, text, re.IGNORECASE)
    if match:        
        return f"31/12/{match.group(1)}" # the date is usually the 31/12 of the year
    
    pattern2 = r"exercice\s+clos\s+le\s+(?::\s*)?(\d{2}\s*[/-]\s*\d{2}\s*[/-]\s*\d{4})"
    match = re.search(pattern2, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return "unknown"

def extract_fiscal_year(text):
    """
    Extracts the fiscal year (usually a 4-digit year).

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The fiscal year, or 'unknown'.
    """
    pattern = r"exercice(?:\s+clos\s+le)?\s*(?::\s*)?(?:\d{2}\s*[/-]\s*\d{2}\s*[/-]\s*)?(\d{4})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return "unknown"

def extract_SIREN(text):
    """
    Extracts the SIREN number (9 digits) from the text.

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The extracted SIREN number, or 'unknown'.
    """
    pattern = r"SIREN\s*[:]?\s*(\d{3}\s*\d{3}\s*\d{3})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return "unknown"

def extract_address(text):
    """
    Extracts a postal address from the text using a generic French format.

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The extracted address, or 'unknown'.
    """
    pattern = r"\d{1,3}\s+[A-Za-zÀ-ÿ\s'-]+,\s*\d{5}\s+[A-Za-zÀ-ÿ\s'-]+"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group().strip()
    return "unknown"

"""function that extracts the amount 
example : resultat totale  56 300.00 
takes the pattern of "resultat totale" as argument and returns the amount
"""

def extract_amount(text, patterns):
    """
    Extracts a monetary amount corresponding to specific text patterns.

    Args:
        text (str): The raw text of the document.
        patterns (list of str): List of regex patterns to locate the amount (e.g., 'total ht').

    Returns:
        str: The extracted amount followed by '€', or 'unknown' if not found.
    """
    amount_pattern = r"[\s:.-]*([\d][\d\s]*(?:[.,]\d+)?)\s*"
    for pattern in patterns:
        pattern = rf"{pattern}{amount_pattern}"
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip()+"€"
    return "unknown"