from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.api.dependency import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register_user(
    payload: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = (
        db.query(User)
        .filter(User.email == payload.email)
        .first()
    )

    if existing_user:
        return {
            "message": "Email already exists"
        }

    user = User(
        name=payload.name,
        email=payload.email
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email
    }