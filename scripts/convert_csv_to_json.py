import pandas as pd
from app.utils import load_data_csv


data_json = load_data_csv().to_json("data/enron_spam_data.json", orient="records", indent=2)

