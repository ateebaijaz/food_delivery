# app/models/restaurant.py
from sqlalchemy import Column, Integer, String, Boolean
from app.database import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=True)
    is_online = Column(Boolean, default=True)
