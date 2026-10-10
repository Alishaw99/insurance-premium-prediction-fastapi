# insurance-premium-prediction-fastapi

# 🛡️ Insurance Premium Category Predictor

A machine learning application that predicts an insurance premium category from user-provided information. FastAPI serves the trained model, while Streamlit provides a colorful, interactive interface.

## Features

- Input validation using Pydantic.
- Automatic calculation of BMI, age group, lifestyle risk, and city tier.
- Predictions using a saved scikit-learn model.
- API responses containing a predicted category, model probability, and class probabilities.
- Streamlit interface with a two-column input form.
- Interactive API documentation and a health-check endpoint.

## Technology Stack

- Python
- FastAPI and Uvicorn
- Pydantic
- Streamlit
- pandas
- scikit-learn
- Requests

## Project Structure

```text
insurance-premium-prediction-fastapi/
├── app.py
├── frontend.py
├── requirements.txt
├── README.md
├── .gitignore
├── schema/
│   ├── __init__.py
│   ├── user_input.py
│   └── prediction_response.py
└── model/
    ├── __init__.py
    ├── predict.py
    └── model.pkl
```

## Setup

Open a terminal in the project folder.

### 1. Create and activate an environment

```powershell
conda create -n insure python=3.11 -y
conda activate insure
```

If the environment already exists, activate it:

```powershell
conda activate insure
```

### 2. Install dependencies

```powershell
python -m pip install -r requirements.txt
```

The supplied model was saved with scikit-learn 1.9.1. Use the same version:

```powershell
python -m pip install "scikit-learn==1.9.1"
python -m pip check
```

For reproducible predictions, use the original training environment's dependency versions wherever available.

### 3. Check the saved model

Ensure the trained model exists at:

```text
model/model.pkl
```

Only load pickle files from trusted sources.

## Run the Application

Run the backend and frontend in separate terminals.

### Terminal 1: FastAPI backend

```powershell
conda activate insure
python -m uvicorn app:app --reload --port 8000
```

API documentation:

http://127.0.0.1:8000/docs

Health check:

http://127.0.0.1:8000/health

### Terminal 2: Streamlit frontend

```powershell
conda activate insure
python -m streamlit run frontend.py
```

Open the local URL printed by Streamlit, usually:

http://localhost:8501

For both applications running on the same computer, the frontend uses:

```python
API_URL = "http://127.0.0.1:8000/predict"
```

If deploying the applications separately, configure this URL to point to the reachable backend.

## Prediction Inputs

| Field | Type | Requirement |
|---|---|---|
| `age` | Integer | Greater than 0 and less than 120 |
| `weight` | Number | Weight in kilograms; greater than 0 |
| `height` | Number | Height in meters; greater than 0 and less than 2.5 |
| `income_lpa` | Number | Annual income in lakhs; greater than 0 |
| `smoker` | Boolean | `true` or `false` |
| `city` | String | Used to determine city tier |
| `occupation` | String | One of the supported occupations |

Supported occupations:

- `retired`
- `freelancer`
- `student`
- `government_job`
- `business_owner`
- `unemployed`
- `private_job`

City-tier matching currently uses predefined city lists and is case-sensitive.

## Derived Model Features

The API transforms the inputs into these model features:

- **BMI:** weight divided by height squared.
- **Age group:** young, adult, middle-aged, or senior.
- **Lifestyle risk:** derived from smoking status and BMI.
- **City tier:** determined by predefined city lists.
- **Annual income:** provided as `income_lpa`.
- **Occupation:** the selected occupation.

The preprocessing rules must remain consistent with those used during model training.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/` | API welcome message |
| GET | `/health` | Model loading status and application model version |
| POST | `/predict` | Generate a premium category prediction |

### Example Request

```json
{
  "age": 35,
  "weight": 75,
  "height": 1.75,
  "income_lpa": 12,
  "smoker": false,
  "city": "Mumbai",
  "occupation": "private_job"
}
```

### Response Structure

The response contains these top-level fields:

| Field | Meaning |
|---|---|
| `predicted_category` | Category predicted by the classifier |
| `confidence` | Model probability assigned to the predicted category |
| `class_probabilities` | Mapping of each class label to its model probability |

The category labels depend on the saved model. Model probabilities are not necessarily calibrated measures of real-world certainty.

### Test with Python

With the backend running:

```python
import requests

payload = {
    "age": 35,
    "weight": 75,
    "height": 1.75,
    "income_lpa": 12,
    "smoker": False,
    "city": "Mumbai",
    "occupation": "private_job",
}

response = requests.post(
    "http://127.0.0.1:8000/predict",
    json=payload,
    timeout=30,
)
response.raise_for_status()
print(response.json())
```

## Troubleshooting

### Cannot connect to the backend

Keep Uvicorn running and verify that `/docs` opens. Check that the frontend's `API_URL` points to the correct server and port.

### No module named `schema` or `model.predict`

Confirm that the folders and Python files shown in the project structure exist. Run Uvicorn from the project root.

### Model file not found

Place `model.pkl` inside the `model` folder. The loader resolves its path relative to `model/predict.py`.

### InconsistentVersionWarning

Match the scikit-learn version used to save the model. If recreating that environment is not possible, retrain and export the model in the intended deployment environment.

### HTTP 422

The request failed input validation. Check the response details for the invalid field.

### HTTP 500

Inspect the backend terminal and error response. Confirm that the model supports `predict_proba()` and that its expected features match the input DataFrame.

## Scope

This project demonstrates model serving and API/frontend integration. It predicts a category rather than an exact premium amount and is intended for educational use.

## Author

Syed Ali

## License

See the repository's `LICENSE` file.