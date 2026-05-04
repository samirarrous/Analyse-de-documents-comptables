import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pipeline.api import app # noqa: F401
from pipeline import router
from pipeline.exporter import export_to_json


def run_cli(file_path):
    if not os.path.exists(file_path):
        print("file not found")
        return

    result = router.route_document(file_path)

    filename = os.path.splitext(os.path.basename(file_path))[0] + ".json"
    output_path = export_to_json(result, filename)

    print(f"result exported : {output_path}")


def main():
    if len(sys.argv) > 1:
        run_cli(sys.argv[1])
    else:
        import uvicorn
        uvicorn.run("main:app", host="0.0.0.0", port=8000)


if __name__ == "__main__":
    main()