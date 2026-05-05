"""
Main entry point for the Accounting Document Analyzer application.
Provides both a Command Line Interface (CLI) and a FastAPI web server.
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.pipeline.api import app # noqa: F401
from src.pipeline import router
from src.pipeline.exporter import export_to_json


def run_cli(file_path):
    """
    Executes the document analysis pipeline from the command line.

    Args:
        file_path (str): The path to the PDF document to be analyzed.

    Returns:
        None: The output is exported directly to a JSON file.
    """
    if not os.path.exists(file_path):
        print("file not found")
        return

    result = router.route_document(file_path)
    # tried to add filename in beginning as requested, but it gave a wrong filename
    base_name = os.path.basename(file_path)
    final_result = {
        "file_name": base_name, #putting filename in the beginning
        **result
    }

    json_filename = os.path.splitext(base_name)[0] + ".json"
    output_path = export_to_json(final_result, json_filename)

    print(f"result exported : {output_path}")


def main():
    """
    Main execution function.
    If a file path is provided as a command-line argument, runs the CLI.
    Otherwise, starts the FastAPI web server on port 8000.
    """
    if len(sys.argv) > 1:
        run_cli(sys.argv[1])
    else:
        import uvicorn
        uvicorn.run("src.main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()