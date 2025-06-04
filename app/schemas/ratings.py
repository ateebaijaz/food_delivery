from typing import Annotated
from pydantic import BaseModel, Field

class RatingInput(BaseModel):
    restaurant_rating: Annotated[int, Field(ge=1, le=5)]
    delivery_agent_rating: Annotated[int, Field(ge=1, le=5)] | None = None


from typing import Optional, List

class RatingResponse(BaseModel):
    order_id: int
    restaurant_rating: int
    delivery_agent_rating: Optional[int] = None
    rated_by_user_id: int
    rated_by_user_name: str  #
    restaurant_name: str
    order_items: List[str]   # ateeb-learning --in fastapi we prepare schema similar to django serializers

    class Config:
        orm_mode = True
