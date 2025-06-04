from app.models.delivery import DeliveryAgent
from sqlalchemy.orm import Session

def assign_delivery_agent(db: Session):
    return db.query(DeliveryAgent).filter_by(is_available=True).first()
