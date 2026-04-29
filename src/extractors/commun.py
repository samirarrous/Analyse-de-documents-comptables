import re
import sys
import os

# Ajouter le dossier parent au chemin
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def extract_document_type(text):
    # different pattern for each type
    patterns = [
        r"compte\s+de\s+résultat",
        r"bilan",
        r"facture",
        r"liasse\s+fiscale",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group().lower()  
    return "unknown"

def extract_date(text):
    pattern = r"\d{2}\s*[/-]\s*\d{2}\s*[/-]\s*\d{4}"
    match = re.search(pattern, text)
    if match:
        return match.group()
    return "unknown"

""" the company name is often before the jurridical form, but not always,
 so i noticed that it's either the document type or the company name that is on the first line,
 so i decided to check if the first line contains the document type, 
 if it does, then we will search for the company name in the rest of the text,
 otherwise we will consider that the first line as the company name, 
"""

def extract_company_name(text):
    pattern = r"(?:DE\s*:\s*)?([A-ZÀ-ÿ0-9\s'&-]+?)\s+(?:EURL|SARL|SAS|SA|SCI|EI)"
    lines = text.split("\n")[:1] 
    if  lines:
        first_line = lines[0]
        if extract_document_type(first_line) == "unknown":
            match = re.search(pattern, first_line, re.IGNORECASE)
            if match:
                return match.group(1).strip()
            else:
                return first_line.strip()
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()
    return "unknown"

def extract_juridical_form(text):
    pattern = r"\b(EURL|SARL|SAS|SA|SCI|EI)\b"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).upper()  
    return "unknown"

def extract_fiscal_year_end_date(text):
    pattern1 = r"exercice\s+(?::\s*)?(\d{4})"
    match = re.search(pattern1, text, re.IGNORECASE)
    if match:        
        return f"31/12/{match.group(1)}" # the date is usually the 31/12 of the year
    
    pattern2 = r"exercice\s+clos\s+le\s+(?::\s*)?(\d{2}\s*[/-]\s*\d{2}\s*[/-]\s*\d{4})"
    match = re.search(pattern2, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return "unknown"

def extract_SIREN(text):
    pattern = r"SIREN\s*[:]?\s*(\d{3}\s*\d{3}\s*\d{3})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return "unknown"

def extract_address(text):
    pattern = r"\d{1,3}\s+[A-Za-zÀ-ÿ\s'-]+,\s*\d{5}\s+[A-Za-zÀ-ÿ\s'-]+"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group().strip()
    return "unknown"
