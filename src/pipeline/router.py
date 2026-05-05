"""
Main routing logic that orchestrates document extraction.
Determines document type and applies the appropriate field extractor.
"""
import os
import sys


from src.field_extractors import bilan
from src.field_extractors import compte_resultat
from src.field_extractors import facture
from src.field_extractors import liasse_fiscale
import src.field_extractors.commun as commun
from src.readers import pdf_type
from src.readers import text_extractor
from src.readers import table_fields_extractor as table


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
    tables = table.extract_tables(file)
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