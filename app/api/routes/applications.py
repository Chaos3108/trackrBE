from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.application import Application
from app.models.user import User

from app.schemas.application import ApplicationCreate

from app.api.dependencies import get_db
from app.api.auth import get_current_user

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post("/")
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # compute next per-user id
    max_user_app_id = (
        db.query(func.max(Application.user_app_id))
        .filter(Application.user_id == current_user.id)
        .scalar()
    )

    next_user_app_id = (max_user_app_id or 0) + 1

    application = Application(
        company=payload.company,
        role=payload.role,
        status=payload.status,
        location=payload.location,
        salary=payload.salary,
        notes=payload.notes,
        user_id=current_user.id,
        user_app_id=next_user_app_id
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application


@router.get("/")
def get_applications(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    applications = (
        db.query(Application)
        .filter(Application.user_id == current_user.id)
        .order_by(Application.user_app_id)
        .all()
    )

    return applications

@router.get("/{user_app_id}")
def get_application(
    user_app_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    application = (
        db.query(Application)
        .filter(
            Application.user_id == current_user.id,
            Application.user_app_id == user_app_id
        )
        .first()
    )

    if not application:
        raise HTTPException(status_code=404, detail="Application not found")

    return application