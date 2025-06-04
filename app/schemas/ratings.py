from typing import Annotated
from pydantic import BaseModel, Field

class RatingInput(BaseModel):
    restaurant_rating: Annotated[int, Field(ge=1, le=5)]
    delivery_agent_rating: Annotated[int, Field(ge=1, le=5)] | None = None


from pydantic import BaseModel
from typing import Optional

class RatingResponse(BaseModel):
    order_id: int
    restaurant_rating: int
    delivery_agent_rating: Optional[int] = None
    rated_by_user_id: int
