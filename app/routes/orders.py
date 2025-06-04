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

from app.schemas.ratings import RatingResponse


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
        raise HTTPException(status_code=403, detail="Youre are not associated with this restaurnet")

    if update.status not in ["accepted", "rejected"]:
        raise HTTPException(status_code=400, detail="Invalid status. Must be 'accepted' or 'rejected'.")

    if order.status != OrderStatus.PENDING:
        raise HTTPException(status_code=400, detail=f"Order already {order.status}, cannot update.")

    order.status = OrderStatus(update.status)
    db.commit()
    return {"message": f"Order {update.status} successfully"}



def get_delivery_agent_by_user(db: Session, user_id: int) -> DeliveryAgent:
    return db.query(DeliveryAgent).filter(DeliveryAgent.user_id == user_id).first()

@router.patch("/{order_id}/deliver")
def mark_order_delivered(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Step 1: Get delivery agent record linked to this user
    delivery_agent = get_delivery_agent_by_user(db, current_user.id)
    if not delivery_agent:
        raise HTTPException(status_code=403, detail="You are not a registered delivery agent")

    # Step 2: Fetch the order
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    # Step 3: Ensure this delivery agent is assigned to the order
    if order.delivery_agent_id != delivery_agent.id:
        raise HTTPException(status_code=403, detail="You are not assigned to this order")

    # Step 4: Mark it as delivered
    order.status = "DELIVERED"
    delivery_agent.is_available = True
    db.commit()

    return {"message": "Order marked as delivered"}



from app.models.rating import Rating
from app.schemas.ratings import RatingInput
@router.post("/{order_id}/rate")
def rate_order(
    order_id: int,
    rating_data: RatingInput,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You cannot rate this order as you are not the user who placed it")

    if not order.status == "delivered":
        raise HTTPException(status_code=400, detail="Order not delivered yet")

    existing = db.query(Rating).filter(Rating.order_id == order_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Already rated")

    rating = Rating(
        order_id=order.id,
        restaurant_rating=rating_data.restaurant_rating,
        delivery_agent_rating=rating_data.delivery_agent_rating,
    )
    db.add(rating)
    db.commit()
    return {"message": "Thanks for your feedback!"}


@router.get("/{order_id}/rating", response_model=RatingResponse)
def get_rating(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rating = db.query(Rating).filter(Rating.order_id == order_id).first()

    if not rating:
        raise HTTPException(status_code=404, detail="No rating found for this order")

    order = db.query(Order).filter(Order.id == order_id).first()
    if not order or order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not authorized to view this rating")

    user = db.query(User).filter(User.id == order.user_id).first()
    restaurant = db.query(Restaurant).filter(Restaurant.id == order.restaurant_id).first()

    return RatingResponse(
        order_id=rating.order_id,
        restaurant_rating=rating.restaurant_rating,
        delivery_agent_rating=rating.delivery_agent_rating,
        rated_by_user_id=user.id,
        rated_by_user_name=user.name,
        restaurant_name=restaurant.name,
        order_items=[item.menu_item.name for item in order.items],
    )
