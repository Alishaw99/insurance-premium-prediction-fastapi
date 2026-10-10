from fastapi import FastAPI, HTTPException

from schema.user_input import UserInput
from schema.prediction_response import PredictionResponse
from model.predict import predict_output, model, MODEL_VERSION

app = FastAPI()


@app.get("/")
def home():
    return {"message": "Insurance Premium Prediction API"}


@app.get("/health")
def health_check():
    return {
        "status": "OK",
        "version": MODEL_VERSION,
        "model_loaded": model is not None,
    }


@app.post("/predict", response_model=PredictionResponse)
def predict_premium(data: UserInput):
    user_input = {
        "bmi": data.bmi,
        "age_group": data.age_group,
        "lifestyle_risk": data.lifestyle_risk,
        "city_tier": data.city_tier,
        "income_lpa": data.income_lpa,
        "occupation": data.occupation,
    }

    try:
        return predict_output(user_input)
    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {error}",
        ) from error