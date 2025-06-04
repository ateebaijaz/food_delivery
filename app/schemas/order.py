from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.models.order import OrderStatus

class OrderItemCreate(BaseModel):
    menu_item_id: int
    quantity: int

class OrderCreate(BaseModel):
    restaurant_id: int
    items: List[OrderItemCreate]

class OrderItemOut(BaseModel):
    menu_item_id: int
    quantity: int
    price: float

    class Config:
        orm_mode = True

class OrderResponse(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    status: OrderStatus
    delivery_agent_id: Optional[int]
    items: List[OrderItemOut]
    created_at: datetime

    class Config:
        orm_mode = True

# app/schemas/order.py

class OrderUpdateStatus(BaseModel):
    status: str  # validated later
