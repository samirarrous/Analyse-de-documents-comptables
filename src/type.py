import pdfplumber
from enum import Enum

class PDFType(Enum):
    NATIVE = "native"
    SCAN = "scan"
    MIXED = "mixed"

def define_type(file_path):
    has_text = False
    has_image = False

    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            if page.extract_text() :
                has_text = True
            if page.images:  
                has_image = True

    if has_text :
        if has_image:
            return PDFType.MIXED
        return PDFType.NATIVE
    else:
        return PDFType.SCAN            
        
print("PDF type:", define_type("../sample_pdfs/09_liasse_fiscale_technovation_multi.pdf").value)