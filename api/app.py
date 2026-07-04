from fastapi import FastAPI
from api.schema import MushroomInput

import joblib
import pandas as pd
import os

app = FastAPI(
    title="Mushroom Classification API",
    version="1.0.0"
)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "encoders.pkl")

best_model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODER_PATH)


@app.get("/")
def root():
    return {
        "message": "Welcome to Mushroom Classification API"
    }


@app.get("/health")
def health():
    return {
        "status": "OK"
    }


@app.post("/predict")
def predict(data: MushroomInput):

    input_dict = data.model_dump()

    df = pd.DataFrame([input_dict])
    for column in df.columns:
        df[column] = encoders[column].transform(df[column])
    prediction = best_model.predict(df)[0]

    probability = best_model.predict_proba(df)[0]

    label = "poisonous" if prediction == 1 else "edible"

    return {
        "prediction": label,
        "probability": round(float(max(probability)), 4)
    }