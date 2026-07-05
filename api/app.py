from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from api.schema import MushroomInput
from api.database import Base, engine, get_db
from api import crud

import joblib
import pandas as pd
import os

app = FastAPI(
    title="Mushroom Classification API",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "models", "best_model.pkl")
ENCODER_PATH = os.path.join(BASE_DIR, "models", "encoders.pkl")

best_model = joblib.load(MODEL_PATH)
encoders = joblib.load(ENCODER_PATH)

LABEL_MAP = {"e": "edible", "p": "poisonous"}


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
def predict(data: MushroomInput, db: Session = Depends(get_db)):
    input_dict = data.model_dump()

    df = pd.DataFrame([input_dict])
    for column in df.columns:
        df[column] = encoders[column].transform(df[column])

    prediction = best_model.predict(df)[0]
    probabilities = best_model.predict_proba(df)[0]

    poisonous_encoder = encoders["poisonous"]
    class_labels = poisonous_encoder.inverse_transform(best_model.classes_)

    probability_by_class = {
        LABEL_MAP[cls]: round(float(prob), 4)
        for cls, prob in zip(class_labels, probabilities)
    }

    predicted_label = LABEL_MAP[poisonous_encoder.inverse_transform([prediction])[0]]
    confidence = round(float(max(probabilities)), 4)

    crud.create_prediction(
        db=db,
        input_data=input_dict,
        prediction=predicted_label,
        confidence=confidence,
        probabilities=probability_by_class,
    )

    return {
        "prediction": predicted_label,
        "confidence": confidence,
        "probabilities": probability_by_class
    }

@app.get("/history")
def history(limit: int = 20, db: Session = Depends(get_db)):
    records = crud.get_predictions(db, limit=limit)

    return [
        {
            "id": r.id,
            "prediction": r.prediction,
            "confidence": r.confidence,
            "probabilities": {
                "edible": r.prob_edible,
                "poisonous": r.prob_poisonous,
            },
            "created_at": r.created_at.isoformat() if r.created_at else None,
        }
        for r in records
    ]