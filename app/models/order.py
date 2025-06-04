from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database import Base
import enum
from sqlalchemy import Enum as SqlEnum

#ateeb learning- in django we have  one field for orm as well as relationship while in sqlalchemy we have two fields one for orm and one for relationship
class OrderStatus(str, enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    DELIVERED = "delivered"

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    restaurant_id = Column(Integer, ForeignKey("restaurants.id"))
    delivery_agent_id = Column(Integer, ForeignKey("delivery_agents.id"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User")
    restaurant = relationship("Restaurant")
    delivery_agent = relationship("DeliveryAgent", backref="orders")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete")

    status = Column(SqlEnum(OrderStatus), default=OrderStatus.PENDING)


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    menu_item_id = Column(Integer, ForeignKey("menu_items.id"))
    quantity = Column(Integer, default=1)
    price = Column(Float)

    order = relationship("Order", back_populates="items")
    menu_item = relationship("MenuItem")
