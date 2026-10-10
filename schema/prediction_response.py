from pydantic import BaseModel, Field

class PredictionResponse(BaseModel):
    predicted_category: str
    confidence: float = Field(ge=0, le=1)
    class_probabilities: dict[str, float]
from pydantic import BaseModel, Field


class PredictionResponse(BaseModel):
    predicted_category: str = Field(
        ...,
        description="The predicted insurance premium category",
        examples=["High"]
    )

    confidence: float = Field(
        ...,
        ge=0,
        le=1,
        description="Model confidence for the predicted class, from 0 to 1",
        examples=[0.8432]
    )

    class_probabilities: dict[str, float] = Field(
        ...,
        description="Probability distribution across all possible classes",
        examples=[{"Low": 0.01, "Medium": 0.15, "High": 0.84}]
    )