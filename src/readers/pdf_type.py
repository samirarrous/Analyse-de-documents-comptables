"""
Module for determining the type of PDF document (native, scanned, or mixed).
"""
import pdfplumber



def define_type(file_path):
    """
    Analyzes a PDF file to determine its type based on text and image presence.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: 'mixed' if it contains both text and images, 'native' if it contains only text,
             and 'scan' if it contains no extractable text.
    """
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
            return "mixed"
        return "native"
    else:
        return "scan"            
        