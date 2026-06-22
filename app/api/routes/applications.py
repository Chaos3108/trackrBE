from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

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
    application = Application(
        company=payload.company,
        role=payload.role,
        status=payload.status,
        location=payload.location,
        salary=payload.salary,
        notes=payload.notes,
        user_id=current_user.id
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
        .all()
    )

    return applications