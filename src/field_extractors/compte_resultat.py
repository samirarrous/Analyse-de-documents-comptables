"""
Extractor module specific to income statement (compte de résultat) documents.
"""

from src.field_extractors import commun
from src.readers import table_fields_extractor

def extract_fields(text, tables):
    """
    Extracts relevant financial fields from an income statement document.

    Args:
        text (str): The raw text of the document.
        tables (list): Parsed tables extracted from the document.

    Returns:
        dict: A dictionary containing extracted income statement data.
    """
    # defining patterns for the fields we want to extract

    close_year = commun.extract_fiscal_year(text)

    total_produits_exploitation_patterns = {r"total\s+produits\s+d.exploitation"}
    total_charges_exploitation_patterns = {r"total\s+charges\s+d.exploitation"}
    
    resultat_exploitation_patterns = {r"r.sultat\s+d.exploitation"}
    resultat_net_patterns = {r"r.sultat\s+net"}
    
    net_present_patterns = {rf"exercice\s+{close_year}", r"exercice\s+présent", r"exercice\s+en\s+cours"}
    net_precedent_patterns = {rf"exercice\s+{int(close_year)-1}", r"exercice\s+précédent"}
    

    return {
        "document_type": commun.extract_document_type(text),
        "company_name": commun.extract_company_name(text),
        "juridical_form": commun.extract_juridical_form(text),
        "SIREN": commun.extract_SIREN(text),
        "fiscal_year": commun.extract_fiscal_year(text),
        "close_date": commun.extract_fiscal_year_end_date(text),
        "total_produits_d'exploitation": {
            "net_present":   table_fields_extractor.extract_from_table(tables, text, total_produits_exploitation_patterns, net_present_patterns, 1),
            "net_precedent": table_fields_extractor.extract_from_table(tables, text, total_produits_exploitation_patterns, net_precedent_patterns, 2),
        },
        "total_charges_d'exploitation": {
            "net_present":   table_fields_extractor.extract_from_table(tables, text, total_charges_exploitation_patterns, net_present_patterns, 1),
            "net_precedent": table_fields_extractor.extract_from_table(tables, text, total_charges_exploitation_patterns, net_precedent_patterns, 2),
        },
        "resultat_de_l'exercice": {
            "resultat_d'exploitation": {
                "net_present":   table_fields_extractor.extract_from_table(tables, text, resultat_exploitation_patterns, net_present_patterns, 1),
                "net_precedent": table_fields_extractor.extract_from_table(tables, text, resultat_exploitation_patterns, net_precedent_patterns, 2),
            },          
            "resultat_net": {
                "net_present":  table_fields_extractor.extract_from_table(tables, text, resultat_net_patterns, net_present_patterns, 1),
                "net_precedent": table_fields_extractor.extract_from_table(tables, text, resultat_net_patterns, net_precedent_patterns, 2),
            }
        }
    }
