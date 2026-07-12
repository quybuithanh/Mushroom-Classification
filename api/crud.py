from sqlalchemy.orm import Session
from api import models
from sqlalchemy import func, text
from api.models import PredictionHistory


def create_prediction(
    db: Session,
    input_data: dict,
    prediction: str,
    confidence: float,
    probabilities: dict,
) -> models.PredictionHistory:

    record = models.PredictionHistory(
        **input_data,
        prediction=prediction,
        confidence=confidence,
        prob_edible=probabilities.get("edible", 0.0),
        prob_poisonous=probabilities.get("poisonous", 0.0),
    )

    db.add(record)
    db.commit()
    db.refresh(record)

    return record


def get_predictions(db: Session, limit: int = 50):
    return (
        db.query(models.PredictionHistory)
        .order_by(models.PredictionHistory.id.desc())
        .limit(limit)
        .all()
    )

def get_statistics(db):
    total = db.query(PredictionHistory).count()

    edible = db.query(PredictionHistory)\
        .filter(PredictionHistory.prediction == "edible")\
        .count()

    poisonous = db.query(PredictionHistory)\
        .filter(PredictionHistory.prediction == "poisonous")\
        .count()

    avg_confidence = db.query(func.avg(PredictionHistory.confidence)).scalar()

    return {
        "total": total,
        "edible": edible,
        "poisonous": poisonous,
        "avg_confidence": float(avg_confidence or 0)
    }

def delete_all_predictions(db: Session):
    db.execute(text("TRUNCATE TABLE prediction_history"))
    db.commit()