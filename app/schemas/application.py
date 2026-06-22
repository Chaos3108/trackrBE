from typing import Optional
from pydantic import BaseModel


class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: str = "Applied"
    location: Optional[str] = None
    salary: Optional[int] = None
    notes: Optional[str] = None
    user_id: int