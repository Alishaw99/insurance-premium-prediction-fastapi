import pickle
from pathlib import Path

import pandas as pd

MODEL_VERSION = "1.0.0"

# Load the model relative to this file.
MODEL_PATH = Path(__file__).resolve().parent / "model.pkl"

with MODEL_PATH.open("rb") as f:
    model = pickle.load(f)


def predict_output(user_input: dict) -> dict:
    df = pd.DataFrame([user_input])

    predicted_class = model.predict(df)[0]
    probabilities = model.predict_proba(df)[0]

    class_probs = {
        str(label): float(probability)
        for label, probability in zip(model.classes_, probabilities)
    }

    predicted_category = str(predicted_class)

    return {
        "predicted_category": predicted_category,
        "confidence": round(class_probs[predicted_category], 4),
        "class_probabilities": {
            label: round(probability, 4)
            for label, probability in class_probs.items()
        },
    }