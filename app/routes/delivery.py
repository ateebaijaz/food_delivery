from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.delivery import DeliveryAgent
from app.schemas.delivery import DeliveryAgentRegister

router = APIRouter(
    prefix="/delivery",
    tags=["delivery"]
)
@router.post("/register-agent")
def register_as_delivery_agent(
    agent_data: DeliveryAgentRegister,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if not agent_data.agent_phone:
        raise HTTPException(status_code=400, detail="Phone number is required")

    existing_agent = db.query(DeliveryAgent).filter(DeliveryAgent.user_id == current_user.id).first()
    if existing_agent:
        raise HTTPException(status_code=400, detail="You are already registered as a delivery agent")

    new_agent = DeliveryAgent(
        name=current_user.name,
        phone=agent_data.agent_phone,
        is_available=True,
        user_id=current_user.id
    )
    db.add(new_agent)
    db.commit()
    db.refresh(new_agent)

    return {"message": "You have been registered as a delivery agent"}
