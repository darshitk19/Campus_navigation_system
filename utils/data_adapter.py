import json
import os

def adapt_path_data(file_path):
    """
    Loads a JSON file containing path data and adapts it to the required format.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    adapted_data = []

    for item in raw_data.get("paths", []):
        adapted_data.append({
            "start": item.get("start"),
            "end": item.get("end"),
            "coordinates": item.get("coordinates", [])
        })

    return adapted_data
