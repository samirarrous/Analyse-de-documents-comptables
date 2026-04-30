import json
import os

def export_to_json(data, filename="output.json"):
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    output_dir = os.path.join(repo_root, "output")
    os.makedirs(output_dir, exist_ok=True)

    path = os.path.join(output_dir, filename)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    return path