import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
"""
instead of making a function for each field, 
i chose to make a single function that takes the patterns for the row and the column as arguments,

in case there are no tables , i didn't find any better solution to distinguish between the values 
than touse colomn_index as argument, it's a (roue de secours) in case there are no tables,
using the symbol € to reconize a value 

"""

def extract_from_table(tables, text,  row_patterns, col_patterns, col_index):
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
