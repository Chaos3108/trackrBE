from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.models.application import Application
from app.schemas.application import ApplicationCreate

from app.api.dependency import get_db

router = APIRouter(
    prefix="/applications",
    tags=["Applications"]
)


@router.post("/")
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db)
):
    application = Application(
        company=payload.company,
        role=payload.role,
        status=payload.status,
        location=payload.location,
        salary=payload.salary,
        notes=payload.notes,
        user_id=payload.user_id
    )

    db.add(application)
    db.commit()
    db.refresh(application)

    return application

@router.get("/")
def get_applications(
    db: Session = Depends(get_db)
):
    applications = (
        db.query(Application)
        .all()
    )

    return applications
