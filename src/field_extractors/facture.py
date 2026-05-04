"""
Extractor module specific to invoice (facture) documents.
"""
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from field_extractors import commun


def extract_facture_number(text):
    """
    Extracts the invoice number from the document.

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The extracted invoice number, or 'unknown'.
    """
    pattern = r"n\s*°?\s*:?\s*((?:[A-Z]+\s*[-/]\s*)?\d{4}\s*[-/]\s*\d{3,4})"
                             # optional ° or : after N   
                             # \s* in case OCR added spaces (AB   -   2026 - 001)
                             # [-/] to match - or / 
                             # [A-Z]* optional letters
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).upper()
    return "unknown"
    
def extract_limit_date(text):
    """
    Extracts the due date (échéance) of the invoice.

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The extracted limit date, or 'unknown'.
    """
    pattern = r"(échéance|avant le|limite) \s*:\s*(\d{2}\s*[/-]\s*\d{2}\s*[/-]\s*\d{4})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(2)  
    return "unknown"

def extract_SIRET(text):
    """
    Extracts the SIRET number (14 digits) from the text.

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The extracted SIRET number, or 'unknown'.
    """
    pattern = r"SIRET\s*[:]?\s*(\d{3}\s*\d{3}\s*\d{3}\s*\d{5})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)
    return "unknown"

def extract_tva_number(text):
    """
    Extracts the intra-community VAT number.

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The extracted VAT number, or 'unknown'.
    """
    pattern = r"TVA\s*([A-ZÀ-ÿ\s'-:]+?)\s*([A-Z]{2}\s*\d{2}\s*\d{3}\s*\d{3})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(2)
    return "unknown"

def extract_total_ht(text):
    """
    Extracts the total amount excluding taxes (Total HT).

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The extracted HT amount, or 'unknown'.
    """
    patterns = [r"total\s+ht"]
    return commun.extract_amount(text, patterns)


def extract_total_ttc(text):
    """
    Extracts the total amount including taxes (Total TTC).

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The extracted TTC amount, or 'unknown'.
    """
    patterns = [r"total\s+ttc", r"\bttc\b"]
    return commun.extract_amount(text, patterns)


def extract_tva_percentage_and_amount(text):
    """
    Extracts both the VAT percentage and the VAT amount.

    Args:
        text (str): The raw text of the document.

    Returns:
        dict: A dictionary with 'percentage' and 'amount' keys.
    """
    result = {}

    percentage_pattern = r"tva.*?(\d{1,2}(?:[.,]\d{1,2})?)\s*%"
    tva_amount_pattern = r"tva.*?\d{1,2}(?:[.,]\d{1,2})?\s*%"
    match = re.search(percentage_pattern, text, re.IGNORECASE)
     
    if match :
        result["percentage"] = match.group(1).strip() + "%"
    else :
        result["percentage"] = "unknown"

    amount = commun.extract_amount(text, [tva_amount_pattern])
    result["amount"] = amount

    return result


def extract_fields(text):
    """
    Extracts all relevant fields for an invoice document.

    Args:
        text (str): The raw text of the document.

    Returns:
        dict: A dictionary containing extracted invoice data.
    """
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
