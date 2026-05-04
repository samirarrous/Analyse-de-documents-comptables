"""
Extractor module specific to tax return (liasse fiscale) documents.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from field_extractors import commun
from readers import table_fields_extractor

def extract_result_before_taxes(text):
    """
    Extracts the result before taxes (résultat avant impôts).

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The extracted amount, or 'unknown'.
    """
    patterns = [r"avant\s+imp[oôéèe]t"]
    return commun.extract_amount(text, patterns)


def extract_result_after_taxes(text):
    """
    Extracts the result after taxes (résultat après impôts).

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The extracted amount, or 'unknown'.
    """
    patterns = [r"apr[eéè]s\s+imp[oôé]t"]
    return commun.extract_amount(text, patterns)


def extract_fiscal_result(text):
    """
    Extracts the fiscal result (résultat fiscal).

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The extracted amount, or 'unknown'.
    """
    patterns = [
        r"r[ée]sultat\s+fiscal",
    ]
    return commun.extract_amount(text, patterns)


def extract_corporate_tax(text):
    """
    Extracts the corporate tax amount (impôt sur les sociétés).

    Args:
        text (str): The raw text of the document.

    Returns:
        str: The extracted amount, or 'unknown'.
    """
    patterns = [
        r"les\s+soci[eé]t[eé]s",
        r"les\s+soci[eé]t[eé]s\s+\(?\d{1,2}\s*%\)?",
        r"imp[oôé]t\s+soci[eé]t[eé]"
    ]
    return commun.extract_amount(text, patterns)

def extract_fields(text, tables):
    """
    Extracts relevant financial fields from a tax return document.

    Args:
        text (str): The raw text of the document.
        tables (list): Parsed tables extracted from the document.

    Returns:
        dict: A dictionary containing extracted tax return data.
    """

    close_year = commun.extract_fiscal_year(text)
    total_actif_patterns = {r"total\s+actif"}
    total_passif_patterns = {r"total\s+passif"}
    net_present_patterns = {r"net\s+présent", rf"net\s+{close_year}"}

    return {
        "document_type": commun.extract_document_type(text),
        "company_name": commun.extract_company_name(text),
        "juridical_form": commun.extract_juridical_form(text),
        "SIREN": commun.extract_SIREN(text),
        "close_date": commun.extract_fiscal_year_end_date(text),
        "total_actif": {
            "net_present":   table_fields_extractor.extract_from_table(tables, text, total_actif_patterns, net_present_patterns, 3),
        },
        "total_passif": {
            "net_present":   table_fields_extractor.extract_from_table(tables, text, total_passif_patterns, net_present_patterns, 3),
        },
        "financial_results": {
            "before_tax": extract_result_before_taxes(text),
            "after_tax": extract_result_after_taxes(text),
            "fiscal_result": extract_fiscal_result(text),
            "corporate_tax": extract_corporate_tax(text),
        }
    }
