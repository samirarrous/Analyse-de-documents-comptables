"""
Extractor module specific to balance sheet (bilan) documents.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from field_extractors import commun
from readers import table_fields_extractor


def extract_fields(text, tables):
    """
    Extracts relevant financial fields from a balance sheet document.

    Args:
        text (str): The raw text of the document.
        tables (list): Parsed tables extracted from the document.

    Returns:
        dict: A dictionary containing extracted balance sheet data (e.g., assets, liabilities).
    """
    
    close_year = commun.extract_fiscal_year(text)
    total_actif_patterns = {r"total\s+actif"}
    total_passif_patterns = {r"total\s+passif"}

    net_present_patterns = {r"net\s+présent", rf"net\s+{close_year}"}
    net_precedent_patterns = {r"net\s+précédent", rf"net\s+{int(close_year)-1}"}

    return {
        "document_type": commun.extract_document_type(text),
        "company_name": commun.extract_company_name(text),
        "juridical_form": commun.extract_juridical_form(text),
        "SIREN": commun.extract_SIREN(text),
        "close_date": commun.extract_fiscal_year_end_date(text),
        "fiscal_year": commun.extract_fiscal_year(text),
        "total_actif": {
            "net_present":   table_fields_extractor.extract_from_table(tables, text, total_actif_patterns, net_present_patterns, 3),
            "net_precedent": table_fields_extractor.extract_from_table(tables, text, total_actif_patterns, net_precedent_patterns, 4),
        },
        "total_passif": {
            "net_present":   table_fields_extractor.extract_from_table(tables, text, total_passif_patterns, net_present_patterns, 3),
            "net_precedent": table_fields_extractor.extract_from_table(tables, text, total_passif_patterns, net_precedent_patterns, 4),
        }
    }
