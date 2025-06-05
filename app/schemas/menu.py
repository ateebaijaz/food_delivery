from pydantic import BaseModel
from typing import Optional

class MenuItemUpdate(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    available: Optional[bool] = None