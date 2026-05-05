"""
Module for extracting text and tables from PDF documents using pdfplumber and OCR (pytesseract).
"""
import pdfplumber
import pdf2image
import pytesseract


def extract_text(file_path):
    """
    Extracts all text from a PDF, combining native text and OCR for images.

    Iterates through each page of the PDF. If native text is found, it is extracted.
    If images are present on the page, OCR is applied to extract text from them.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        str: The complete extracted text from the document.
    """
    text = ""

    with pdfplumber.open(file_path) as pdf:
        for i in range(len(pdf.pages)):
            page = pdf.pages[i]
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
            # convert the scanned page to image and extract text from it
            elif page.images:
                image = pdf2image.convert_from_path(file_path, first_page=i+1, last_page=i+1)[0]
                text += pytesseract.image_to_string(image) + "\n"
    return text

