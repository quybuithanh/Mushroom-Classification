from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from api.schema import MushroomInput, MushroomBatchInput
from api.database import Base, engine, get_db
from api import crud
from fastapi.responses import FileResponse
import tempfile

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

@app.get("/model-info")
def model_info():
    poisonous_encoder = encoders["poisonous"]
    class_names = [LABEL_MAP[c] for c in poisonous_encoder.inverse_transform(best_model.classes_)]

    params = best_model.get_params()
    
    feature_importances = {
        feature: round(float(importance), 4)
        for feature, importance in zip(best_model.feature_names_in_, best_model.feature_importances_)
    }

    return {
        "model_type": type(best_model).__name__,
        "n_estimators": params.get("n_estimators"),
        "criterion": params.get("criterion"),
        "max_depth": params.get("max_depth"),
        "random_state": params.get("random_state"),
        "n_features": int(best_model.n_features_in_),
        "features": list(best_model.feature_names_in_),
        "classes": class_names,
        "feature_importances": feature_importances,
    }

def run_prediction(input_dict: dict):

    df = pd.DataFrame([input_dict])
    df["stalk_root"] = df["stalk_root"].replace("?", "b")

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

    return predicted_label, confidence, probability_by_class

@app.post("/predict")
def predict(data: MushroomInput, db: Session = Depends(get_db)):
    input_dict = data.model_dump()
    predicted_label, confidence, probability_by_class = run_prediction(input_dict)
    
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

@app.post("/predict/batch")
def predict_batch(data: MushroomBatchInput, db: Session = Depends(get_db)):
    results = []

    for item in data.items:
        input_dict = item.model_dump()

        predicted_label, confidence, probability_by_class = run_prediction(input_dict)

        crud.create_prediction(
            db=db,
            input_data=input_dict,
            prediction=predicted_label,
            confidence=confidence,
            probabilities=probability_by_class,
        )

        results.append({
            "input": input_dict,
            "prediction": predicted_label,
            "confidence": confidence,
            "probabilities": probability_by_class,
        })

    return {
        "count": len(results),
        "results": results,
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

@app.get("/stats")
def statistics(db: Session = Depends(get_db)):
    return crud.get_statistics(db)

@app.delete("/history")
def delete_history(db: Session = Depends(get_db)):
    crud.delete_all_predictions(db)
    return {"message": "Đã xóa toàn bộ lịch sử dự đoán."}