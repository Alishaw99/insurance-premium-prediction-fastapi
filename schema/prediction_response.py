from pydantic import BaseModel, Field

class PredictionResponse(BaseModel):
    predicted_category: str
    confidence: float = Field(ge=0, le=1)
    class_probabilities: dict[str, float]
