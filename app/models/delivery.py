# app/models/delivery_agent.py
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
class DeliveryAgent(Base):
    __tablename__ = "delivery_agents"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True, nullable=False)
    is_available = Column(Boolean, default=True)

    user_id = Column(Integer, ForeignKey("users.id"), unique=True)  
    user = relationship("User")
