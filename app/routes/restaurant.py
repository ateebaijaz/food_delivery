from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.restaurant import Restaurant, MenuItem
from app.schemas.restaurant import (
    RestaurantCreate, Restaurant as RestaurantSchema,
    MenuItemCreate, MenuItem as MenuItemSchema,
)
from app.schemas.restaurant import RestaurantUpdate

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

# Create a new restaurant owned by current user
@router.post("/", response_model=RestaurantSchema)
def create_restaurant(
    restaurant_data: RestaurantCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurant = Restaurant(
        name=restaurant_data.name,
        address=restaurant_data.address,
        is_online=restaurant_data.is_online,
        owner_id=current_user.id,
    )
    db.add(restaurant)
    db.commit()
    db.refresh(restaurant)
    return {"Message": "Restaurant created successfully", "restaurant": {
        "id": restaurant.id,
        "name": restaurant.name,
        "address": restaurant.address,
        "is_online": restaurant.is_online,
        "owner_id": restaurant.owner_id, 
    }}

# List all restaurants owned by current user
@router.get("/", response_model=List[RestaurantSchema])
def list_restaurants(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurants = db.query(Restaurant).filter(Restaurant.owner_id == current_user.id).all()
    return restaurants

# Add menu item to a restaurant
@router.post("/{restaurant_id}/menu_items/", response_model=MenuItemSchema)
def add_menu_item(
    restaurant_id: int,
    menu_item_data: MenuItemCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # Verify the restaurant belongs to current user
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id, Restaurant.owner_id == current_user.id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found or not owned by user")

    menu_item = MenuItem(
        name=menu_item_data.name,
        price=menu_item_data.price,
        available=menu_item_data.available,
        restaurant_id=restaurant_id,
    )
    db.add(menu_item)
    db.commit()
    db.refresh(menu_item)
    return menu_item

# List menu items of a restaurant
@router.get("/{restaurant_id}/menu_items/", response_model=List[MenuItemSchema])
def list_menu_items(
    restaurant_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id, Restaurant.owner_id == current_user.id).first()
    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found or not owned by user")

    return db.query(MenuItem).filter(MenuItem.restaurant_id == restaurant_id).all()


@router.get("/online")
def get_online_restaurants(db: Session = Depends(get_db)):
    restaurants = db.query(Restaurant).filter(Restaurant.is_online == True).all()
    return restaurants




@router.patch("/{restaurant_id}")
def update_restaurant(
    restaurant_id: int,
    updates: RestaurantUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    restaurant = db.query(Restaurant).filter(Restaurant.id == restaurant_id).first()

    if not restaurant:
        raise HTTPException(status_code=404, detail="Restaurant not found")

    if restaurant.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="You are not the owner of this restaurant")

    if updates.name is not None:
        restaurant.name = updates.name
    if updates.address is not None:
        restaurant.address = updates.address
    if updates.is_online is not None:
        restaurant.is_online = updates.is_online

    db.commit()
    db.refresh(restaurant)
    return {"message": "Restaurant updated", "restaurant": {
        "id": restaurant.id,
        "name": restaurant.name,
        "is_online": restaurant.is_online
    }}