from fastapi import APIRouter, Depends
from app.models.user import User
from app.dependencies.auth import get_current_user

router = APIRouter(prefix="/user", tags=["user"])

@router.get("/me")
def read_me(current_user: User = Depends(get_current_user)):
    return {
        "id": current_user.id,
        "name": current_user.name,
        "email": current_user.email,
    }
