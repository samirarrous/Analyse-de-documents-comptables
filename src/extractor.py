import pdfplumber
import pdf2image
import pytesseract


def extract_text(file_path):
    text = ""

    with pdfplumber.open(file_path) as pdf:
        images = pdf2image.convert_from_path(file_path)

        for i in range(len(pdf.pages)): 
            page_text = pdf.pages[i].extract_text() # using index to insure the order of text and images
            if page_text:
                text += page_text + "\n"

            if pdf.pages[i].images:
                text += pytesseract.image_to_string(images[i]) + "\n"

    return text

def extract_tables(file_path):  # direct extraction of tables if possible (native or mixed) 
    with pdfplumber.open(file_path) as pdf:
        tables = []
        for page in pdf.pages:
            tables.extend(page.extract_tables())
        return tables
    
