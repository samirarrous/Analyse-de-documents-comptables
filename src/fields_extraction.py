import re
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
