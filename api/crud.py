from sqlalchemy.orm import Session
from api import models

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