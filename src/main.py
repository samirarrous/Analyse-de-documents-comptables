from text_extractor import extract_text, extract_tables
from pipeline.router import route_document
from pipeline.exporter import export_to_json

file = "../sample_pdfs/06_bilan_delices_scan.pdf"
fields = route_document(file)

path = export_to_json(fields)

print(export_to_json(fields))