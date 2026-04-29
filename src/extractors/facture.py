import re
import sys
import os

# Ajouter le dossier parent au chemin
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def extract_facture_number(text):
    pattern = r"n\s*°?\s*:?\s*((?:[A-Z]+\s*[-/]\s*)?\d{4}\s*[-/]\s*\d{3,4})"# example: N° ABC-2024-001
                             # optional ° or : after N   
                             # \s* in case OCR added spaces (AB   -   2026 - 001)
                             # [-/] to match - or / 
                             # [A-Z]* optional letters
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1).upper  
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
