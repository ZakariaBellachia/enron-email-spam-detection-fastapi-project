import joblib
import numpy as np
import sklearn
import os
from typing import Literal
model_path = os.path.join("app", "model", "model.joblib")
tfidf_path = os.path.join("app", "model", "tfidf.joblib")
# Load model and vectorizer once
vect = joblib.load(tfidf_path)
model = joblib.load(model_path)


def predict_email(text: str) -> Literal["spam", "ham"]:
    text_input = vect.transform([text]).toarray()
    pred = model.predict(text_input)[0]
    return "spam" if pred == 1 else "ham"