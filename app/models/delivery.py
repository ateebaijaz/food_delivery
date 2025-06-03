# app/models/delivery_agent.py
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class DeliveryAgent(Base):
    __tablename__ = "delivery_agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    is_available = Column(Boolean, default=True)
