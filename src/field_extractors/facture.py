import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from field_extractors import commun


amount_pattern = r"[\s:.-]*([\d][\d\s]*(?:[.,]\d+)?)\s*"

def extract_facture_number(text):
    pattern = r"n\s*°?\s*:?\s*((?:[A-Z]+\s*[-/]\s*)?\d{4}\s*[-/]\s*\d{3,4})"# example: N° ABC-2024-001
                             # optional ° or : after N   
                             # \s* in case OCR added spaces (AB   -   2026 - 001)
                             # [-/] to match - or / 
                             # [A-Z]* optional letters
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return "unknown"
    
def extract_limit_date(text):
    pattern = r"(échéance|avant le|limite) \s*:\s*(\d{2}\s*[/-]\s*\d{2}\s*[/-]\s*\d{4})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(2)  
    return "unknown"

def extract_SIRET(text):
    pattern = r"SIRET\s*[:]?\s*(\d{3}\s*\d{3}\s*\d{3}\s*\d{5})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return "unknown"

def extract_tva_number(text):
    pattern = r"TVA\s*([A-ZÀ-ÿ\s'-:]+?)\s*([A-Z]{2}\s*\d{2}\s*\d{3}\s*\d{3})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(2)
    return "unknown"

def extract_total_ht(text):
    pattern = rf"total\s+ht{amount_pattern}"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()+"€"
    return "unknown"

def extract_total_ttc(text):
    pattern = rf"ttc{amount_pattern}"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).strip()+"€"
    return "unknown"


def extract_tva_percentage_and_amount(text):
    result = {}
    percentage_pattern = r"tva.*?(\d{1,2}(?:[.,]\d{1,2})?)\s*%"
    tva_amount_pattern = rf"{percentage_pattern}{amount_pattern}"
    match = re.search(percentage_pattern, text, re.IGNORECASE)
    if match:
        result["percentage"] = match.group(1).strip() + "%"
    else:
        result["percentage"] = "unknown"
    match = re.search(tva_amount_pattern, text, re.IGNORECASE)
    if match:
        result["amount"] = match.group(2).strip() + "€"
    else:
        result["amount"] = "unknown"
    return result

def extract_facture_fields(text):
     return {
        "document_type": commun.extract_document_type(text),
        "company_name": commun.extract_company_name(text),
        "facture_number": extract_facture_number(text),
        "limit_date": extract_limit_date(text),
        "SIRET": extract_SIRET(text),
        "tva_number": extract_tva_number(text),
        "total_ht": extract_total_ht(text),
        "total_ttc": extract_total_ttc(text),
        "tva": extract_tva_percentage_and_amount(text)
     }
