import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
"""
instead of making a function for each field, 
i chose to make a single function that takes the pattern and the column index as parameters
"""
def extract_from_table(tables, text,  row_pattern, col_index):
    if tables:
        for table in tables:
            for row in table:
                for cell in range(len(row)):
                    if re.search(row_pattern, row[cell], re.IGNORECASE):
                        return row[cell + col_index].strip()
    else:
        amount = r"[\d][\d\s,.]*[€e]"       
        separator = r".*?"    
        text_pattern = rf"{row_pattern}{separator}(?:{separator}{amount}){{{col_index-1}}}{separator}([\d\s,.-]+{amount})"
        match = re.search(text_pattern, text, re.IGNORECASE)
        if match:
            return match.group(1).strip().replace("e", "€")
    return "unknown"
