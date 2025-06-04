from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.order import Order, OrderItem
from app.models.restaurant import MenuItem, Restaurant
from app.models.delivery import DeliveryAgent
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse
from app.utils.delivery import assign_delivery_agent
from app.schemas.order import OrderUpdateStatus

from app.models.order import Order, OrderStatus


router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("/", response_model=OrderResponse)
def place_order(order_data: OrderCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)):
    # Check restaurant exists
    restaurant = db.query(Restaurant).filter_by(id=order_data.restaurant_id, is_online=True).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not available")

    # Validate and prepare order items
    order_items = []
    for item in order_data.items:
        menu_item = db.query(MenuItem).filter_by(id=item.menu_item_id, restaurant_id=order_data.restaurant_id).first()
        if not menu_item or not menu_item.available:
            raise HTTPException(status_code=400, detail=f"Invalid menu item: {item.menu_item_id}")
        order_items.append(OrderItem(menu_item_id=menu_item.id, quantity=item.quantity, price=menu_item.price))

    # Auto-assign delivery agent
    agent = assign_delivery_agent(db)
    if not agent:
        raise HTTPException(status_code=503, detail="No delivery agents available. Please try again later.")

    # Create order
    order = Order(user_id=user.id, restaurant_id=restaurant.id, delivery_agent_id=agent.id)
    db.add(order)
    db.flush()

    for item in order_items:
        item.order_id = order.id
        db.add(item)

    # Mark agent unavailable
    agent.is_available = False

    db.commit()
    db.refresh(order)
    return order


# app/routes/orders.py




@router.patch("/{order_id}/status")
def update_order_status(order_id: int, update: OrderUpdateStatus, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to update this order")

    if update.status not in ["accepted", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'accepted' or 'rejected'.")

    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail=f"Order already {order.status}, cannot update.")

    order.status = OrderStatus(update.status)
    db.commit()
    return {"message": f"Order {update.status} successfully"}



@router.patch("/{order_id}/deliver")
def mark_order_delivered(order_id: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Check agent is assigned
    if not order.delivery_agent_id:
        raise HTTPException(status_code=400, detail="No delivery agent assigned to this order")
    
    agent = db.query(DeliveryAgent).filter(DeliveryAgent.id == order.delivery_agent_id).first()
    
    if str(agent.id) != str(current_user.id):  # Assuming delivery agents log in via same system
        raise HTTPException(status_code=403, detail="You are not assigned to this order")

    if order.status != OrderStatus.ACCEPTED:
        raise HTTPException(status_code=400, detail="Order not in accepted state")

    order.status = OrderStatus.DELIVERED
    agent.is_available = True
    db.commit()
    return {"message": "Order marked as delivered"}