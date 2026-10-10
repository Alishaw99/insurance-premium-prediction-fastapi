import pickle
from pathlib import Path

import pandas as pd

# Application model version; change when you replace the model.
MODEL_VERSION = "1.0.0"

MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"

with MODEL_PATH.open("rb") as file:
    model = pickle.load(file)


def predict_output(user_input: dict) -> dict:
    input_df = pd.DataFrame([user_input])

    prediction = model.predict(input_df)[0]
    probabilities = model.predict_proba(input_df)[0]

    class_probabilities = {
        str(label): float(probability)
        for label, probability in zip(model.classes_, probabilities)
    }

    predicted_category = str(prediction)

    return {
        "predicted_category": predicted_category,
        "confidence": class_probabilities[predicted_category],
        "class_probabilities": class_probabilities,
    }