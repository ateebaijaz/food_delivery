from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.restaurant import Restaurant, MenuItem
from app.models.user import User
from app.schemas.menu import MenuItemUpdate
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/menu", tags=["menu"])

@router.patch("/{menu_item_id}")
def update_menu_item(
    menu_item_id: int,
    updates: MenuItemUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    item = db.query(MenuItem).filter(MenuItem.id == menu_item_id).first()

    if not item:
        raise HTTPException(status_code=404, detail="Menu item not found")

    restaurant = db.query(Restaurant).filter(Restaurant.id == item.restaurant_id).first()
    if restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You do not own this restaurant")

    if updates.name is not None:
        item.name = updates.name
    if updates.price is not None:
        item.price = updates.price
    if updates.available is not None:
        item.available = updates.available

    db.commit()
    db.refresh(item)
    return {"message": "Menu item updated", "menu_item": {
        "id": item.id,
        "name": item.name,
        "price": item.price,
        "available": item.available
    }}
