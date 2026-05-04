"""
Main routing logic that orchestrates document extraction.
Determines document type and applies the appropriate field extractor.
"""
import os
import sys


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from field_extractors import bilan
from field_extractors import compte_resultat
from field_extractors import facture
from field_extractors import liasse_fiscale
import field_extractors.commun as commun
import readers.pdf_type as pdf_type
import readers.text_extractor as text_extractor

def route_document(file):
    """
    Routes a PDF document through the analysis pipeline.

    It detects if the PDF is text or image-based, extracts the raw content,
    determines the specific accounting document type, and then routes the 
    data to the corresponding specific extractor (e.g., invoice, balance sheet).

    Args:
        file (str): The path to the PDF document to process.

    Returns:
        dict: The extracted fields including document type and extracted data.
    """
    file_type = pdf_type.define_type(file)
    text = text_extractor.extract_text(file)
    tables = text_extractor.extract_tables(file)
    doc_type = commun.extract_document_type(text)

    fields = {}
    fields["pdf_type"] = file_type
    fields["extracted_data"] = {}
    if doc_type == "bilan":
        fields["extracted_data"] = bilan.extract_fields(text, tables)
    if doc_type == "compte_resultat":
        fields["extracted_data"] = compte_resultat.extract_fields(text, tables)
    if doc_type == "facture":
        fields["extracted_data"] = facture.extract_fields(text)
    if doc_type == "liasse_fiscale":
        fields["extracted_data"] = liasse_fiscale.extract_fields(text, tables)
    return  fields