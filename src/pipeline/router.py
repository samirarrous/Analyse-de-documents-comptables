from extractors.bilan import extract_bilan_fields
import extractors.commun as commun
import pdf_type
import text_extractor

def route_document(file):
    file_type = pdf_type.define_type(file)
    text = text_extractor.extract_text(file)
    tables = text_extractor.extract_tables(file)
    doc_type = commun.extract_document_type(text)

    fields = {}
    fields["pdf_type"] = file_type
    if doc_type == "bilan":
        fields = extract_bilan_fields(text, tables)
    
    return  fields