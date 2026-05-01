import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from field_extractors import commun
from readers import table_fields_extractor


def extract_compte_resultat_fields(text, tables):
    return {
        "document_type": commun.extract_document_type(text),
        "company_name": commun.extract_company_name(text),
        "juridical_form": commun.extract_juridical_form(text),
        "SIREN": commun.extract_SIREN(text),
        "close_date": commun.extract_fiscal_year_end_date(text),
        "total_produits_d'exploitation": {
            "net_present":   table_fields_extractor.extract_from_table(tables, text, r"total\s+produits\s+d.exploitation",  1),
            "net_precedent": table_fields_extractor.extract_from_table(tables, text, r"total\s+produits\s+d.exploitation",  2),
        },
        "total_charges_d'exploitation": {
            "net_present":   table_fields_extractor.extract_from_table(tables, text, r"total\s+charges\s+d.exploitation", 1),
            "net_precedent": table_fields_extractor.extract_from_table(tables, text, r"total\s+charges\s+d.exploitation", 2),
        },
        "total_charges_d'exploitation": {
            "net_present":   table_fields_extractor.extract_from_table(tables, text, r"total\s+charges", 1),
            "net_precedent": table_fields_extractor.extract_from_table(tables, text, r"total\s+charges", 2),
        },
        "resultat_de_l'exercice": {
            "resultat_d'exploitation": {
                "net_present":   table_fields_extractor.extract_from_table(tables, text, r"r.sultat\s+d.exploitation", 1),
                "net_precedent": table_fields_extractor.extract_from_table(tables, text, r"r.sultat\s+d.exploitation", 2),
            },          
            "resultat_net": {
                "net_present":  table_fields_extractor.extract_from_table(tables, text, r"r.sultat\s+net", 1),
                "net_precedent": table_fields_extractor.extract_from_table(tables, text, r"r.sultat\s+net", 2),
            }
        }
    }