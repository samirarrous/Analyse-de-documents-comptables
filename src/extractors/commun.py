import re
import sys
import os

# Ajouter le dossier parent au chemin
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import text_extractor
import pdf_type

def extract_document_type(text):
    # Define patterns for different document types):
    patterns = [
        r"compte\s+de\s+résultat",
        r"bilan",
        r"facture",
        r"liasse\s+fiscale",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            return match.group().lower()  
    return "unknown"

def extract_date(text):
    # Pattern pour les dates au format JJ/MM/AAAA ou JJ-MM-AAAA
    pattern = r"\d{2}\s*[/-]\s*\d{2}\s*[/-]\s*\d{4}"
    match = re.search(pattern, text)
    if match:
        return match.group()
    return "unknown"
