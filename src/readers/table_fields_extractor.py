"""
Module for extracting specific fields from parsed PDF tables or text.
"""
import re
import sys
import os
import pdfplumber

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

"""
instead of making a function for each field, 
i chose to make a single function that takes the patterns for the row and the column as arguments,

in case there are no tables , i didn't find any better solution to distinguish between the values 
than touse colomn_index as argument, it's a (roue de secours) in case there are no tables,
using the symbol € to reconize a value 

"""
def extract_tables(file_path): # direct extraction of tables if possible (native or mixed) 
    """
    Extracts all structural tables from a PDF using pdfplumber.

    Args:
        file_path (str): The path to the PDF file.

    Returns:
        list: A list of tables, where each table is a list of rows, and each row is a list of cells.
    """
    with pdfplumber.open(file_path) as pdf:
        tables = []
        for page in pdf.pages:
            tables.extend(page.extract_tables())
        return tables


def extract_from_table(tables, text,  row_patterns, col_patterns, col_index):
    """
    Extracts a value from a table based on row and column regex patterns.
    If no tables are found, attempts to extract the value directly from the text
    using a fallback regex strategy based on the column index.

    Args:
        tables (list): A list of parsed tables from the PDF.
        text (str): The full raw text of the document.
        row_patterns (list of str): Regex patterns to match the target row.
        col_patterns (list of str): Regex patterns to match the target column header.
        col_index (int): The 1-based index of the target column (used for the text fallback).

    Returns:
        str: The extracted value, or 'unknown' if not found.
    """
    if tables:
        for table in tables:
            for row in table:
                for cell in range(len(row)):
                    for row_pattern in row_patterns:
                        if re.search(row_pattern, str(row[cell]), re.IGNORECASE):
                            # the colomn index > the index of the cell where the row pattern 
                            # for exemple in "liasse fiscale" we have "net 2025" before "total passif" 
                            # so we have to find "net 2025" that is after "total passif" 
                            for colon in range(cell + 1, len(table[0])):  
                                for col_pattern in col_patterns:
                                    if re.search(col_pattern, str(table[0][colon]), re.IGNORECASE):
                                        return row[colon].strip()
    
    amount = r"[\d][\d\s,.]*[€e]"
    separator = r".*?"
    for row_pattern in row_patterns:
        text_pattern = rf"{row_pattern}{separator}(?:{amount}{separator}){{{col_index-1}}}({amount})"
        match = re.search(text_pattern, text, re.IGNORECASE | re.DOTALL)
        if match:
            return match.group(1).strip().replace("e","€")
    return "unknown"
