import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from field_extractors import commun
from readers import table_fields_extractor



def extract_liasse_fiscale_fields(text, tables):

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
        }
    }

