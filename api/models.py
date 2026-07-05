from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from api.database import Base
 
class PredictionHistory(Base): 
    __tablename__ = "prediction_history"
    id = Column(Integer, primary_key=True, index=True)
 
    cap_shape = Column(String(1), nullable=False)
    cap_surface = Column(String(1), nullable=False)
    cap_color = Column(String(1), nullable=False)
    bruises = Column(String(1), nullable=False)
    odor = Column(String(1), nullable=False)
    gill_attachment = Column(String(1), nullable=False)
    gill_spacing = Column(String(1), nullable=False)
    gill_size = Column(String(1), nullable=False)
    gill_color = Column(String(1), nullable=False)
    stalk_shape = Column(String(1), nullable=False)
    stalk_root = Column(String(1), nullable=False)
    stalk_surface_above_ring = Column(String(1), nullable=False)
    stalk_surface_below_ring = Column(String(1), nullable=False)
    stalk_color_above_ring = Column(String(1), nullable=False)
    stalk_color_below_ring = Column(String(1), nullable=False)
    veil_type = Column(String(1), nullable=False)
    veil_color = Column(String(1), nullable=False)
    ring_number = Column(String(1), nullable=False)
    ring_type = Column(String(1), nullable=False)
    spore_print_color = Column(String(1), nullable=False)
    population = Column(String(1), nullable=False)
    habitat = Column(String(1), nullable=False)
 
    # Kết quả dự đoán
    prediction = Column(String(20), nullable=False)
    confidence = Column(Float, nullable=False)
    prob_edible = Column(Float, nullable=False)
    prob_poisonous = Column(Float, nullable=False)
 
    created_at = Column(DateTime(timezone=True), server_default=func.now())