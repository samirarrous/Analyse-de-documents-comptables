import re
import sys
import os

# Ajouter le dossier parent au chemin
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import text_extractor

def extract_facture_number(text):
    # On autorise des espaces partout, même autour du slash
    pattern = r"n\s*°?\s*:?\s*((?:[A-Z]+\s*[-/]\s*)?\d{4}\s*[-/]\s*\d{3,4})"# example: N° ABC-2024-001
                             # optional ° or : after N   
                             # \s* in case OCR added spaces (AB   -   2026 - 001)
                             # [-/] to match - or / 
                             # [A-Z]* optional letters
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)  # Return the captured facture number
    return "unknown"
    
def extract_limit_date(text):
    pattern = r"(échéance|avant le|limite) \s*:\s*(\d{2}\s*[/-]\s*\d{2}\s*[/-]\s*\d{4})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(2)  # Return the captured date
    return "unknown"
print("text :", text_extractor.extract_text("../../sample_pdfs/03_facture_plomberie_scan.pdf"))