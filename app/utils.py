import pandas as pd
import json
import os

# Path relative to project root
DATA_FOLDER = os.path.join("data")

def load_data_csv():
    csv_path = os.path.join(DATA_FOLDER, "enron_spam_data.csv")
    return pd.read_csv(csv_path)

def load_data_json():
    json_path = os.path.join(DATA_FOLDER, "enron_spam_data.json")
    try:
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # If it's a single dict, convert to list
            if isinstance(data, dict):
                return [data]
            return data
    except FileNotFoundError:
        return []  # Return empty list if file missing