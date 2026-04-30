import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extractors import commun


""" to avoid repeating the same code for each field,
i choosed to do it in the same function to browse the table only once 
"""
def extract_from_table(text, tables):
    actif_pattern = r"total\s+actif"
    passif_pattern = r"total\s+passif"

    total_actif_present = None
    total_actif_prec = None
    total_passif_present = None
    total_passif_prec = None

    if tables:
        for table in tables:
            for row in table:
                label = row[0].strip()

                #  ACTIF 
                if re.search(actif_pattern, label, re.IGNORECASE):
                    total_actif_present = row[len(row)-2]
                    total_actif_prec = row[len(row)-1]

                # PASSIF 
                if re.search(passif_pattern, label, re.IGNORECASE):
                    total_passif_present = row[len(row)-2  ]
                    total_passif_prec = row[len(row)-1]

    
    else :
        # sometimes ocr does not reconize the symbol € and replaces it with e
        # so i chose separating numbers with this symbole since it's always present
        # the table in "bilan" 
        amount = r"[€e]"       
        separator = r".*?"          
        
        text_actif_pattern_present = rf"TOTAL\s+ACTIF{separator}(?:{separator}{amount}){{2}}{separator}([\d\s,.-]+{amount})"
        text_actif_pattern_prec    = rf"TOTAL\s+ACTIF{separator}(?:{separator}{amount}){{3}}{separator}([\d\s,.-]+{amount})"

        text_passif_pattern_present = rf"TOTAL\s+PASSIF{separator}(?:{separator}{amount}){{2}}{separator}([\d\s,.-]+{amount})"
        text_passif_pattern_prec    = rf"TOTAL\s+PASSIF{separator}(?:{separator}{amount}){{3}}{separator}([\d\s,.-]+{amount})"
        
        match_actif_present = re.search(text_actif_pattern_present, text, re.IGNORECASE)
        match_actif_prec = re.search(text_actif_pattern_prec, text, re.IGNORECASE)

        match_passif_present = re.search(text_passif_pattern_present, text, re.IGNORECASE)
        match_passif_prec = re.search(text_passif_pattern_prec, text, re.IGNORECASE)

        if match_actif_present:
            total_actif_present = match_actif_present.group(1).strip().replace("e", "€")
        else:
            total_actif_present = "unknown"
        if match_actif_prec:
            total_actif_prec = match_actif_prec.group(1).strip().replace("e", "€")
        else:
            total_actif_prec = "unknown"
        if match_passif_present:
            total_passif_present = match_passif_present.group(1).strip().replace("e", "€")
        else: 
            total_passif_present = "unknown"
        if match_passif_prec:
            total_passif_prec = match_passif_prec.group(1).strip().replace("e", "€")
        else:
            total_passif_prec = "unknown"

    return {
        "total_actif": {
            "net_present": total_actif_present,
            "net_precedent": total_actif_prec
        },
        "total_passif": {
            "net_present": total_passif_present,
            "net_precedent": total_passif_prec
        }
    }



def extract_total_actif_present(text, tables):
    return extract_from_table(text, tables)["total_actif"]["net_present"]

def extract_total_actif_prec(text, tables):
    return extract_from_table(text, tables)["total_actif"]["net_precedent"]

def extract_total_passif_present(text, tables):
    return extract_from_table(text, tables)["total_passif"]["net_present"]

def extract_total_passif_prec(text, tables):
    return extract_from_table(text, tables)["total_passif"]["net_precedent"]


def extract_bilan_fields(text, tables):
    return {
        "document_type": commun.extract_document_type(text),
        "company_name": commun.extract_company_name(text),
        "juridical_form": commun.extract_juridical_form(text),
        "SIREN": commun.extract_SIREN(text),
        "close_date": commun.extract_fiscal_year_end_date(text),
        "total_actif": {
            "net_present": extract_total_actif_present(text, tables),
            "net_precedent": extract_total_actif_prec(text, tables)
        },
        "total_passif": {
            "net_present": extract_total_passif_present(text, tables),
            "net_precedent": extract_total_passif_prec(text, tables)
        }
    }

