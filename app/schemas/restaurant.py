from pydantic import BaseModel
from typing import List, Optional

class MenuItemBase(BaseModel):
    name: str
    price: float
    available: Optional[bool] = True

class MenuItemCreate(MenuItemBase):
    pass

class MenuItem(MenuItemBase):
    id: int

    class Config:
        orm_mode = True

class RestaurantBase(BaseModel):
    name: str
    address: Optional[str] = None
    is_online: Optional[bool] = True

class RestaurantCreate(RestaurantBase):
    pass

class Restaurant(RestaurantBase):
    id: int
    owner_id: int
    menu_items: List[MenuItem] = []

    class Config:
        orm_mode = True

class RestaurantUpdate(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    is_online: Optional[bool] = None
