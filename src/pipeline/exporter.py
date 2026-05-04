"""
Utility module for exporting extracted data to JSON files.
"""
import json
import os

def export_to_json(data, filename="output.json"):
    """
    Exports a dictionary of data to a JSON file in the 'output' directory.

    Args:
        data (dict): The structured data to export.
        filename (str): The name of the output JSON file. Defaults to "output.json".

    Returns:
        str: The absolute path to the generated JSON file.
    """
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    output_dir = os.path.join(repo_root, "output")
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(output_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return path