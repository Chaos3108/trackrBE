from pydantic import BaseModel
from typing import Optional


class ApplicationCreate(BaseModel):
    company: str
    role: str
    status: str = "Applied"
    location: Optional[str] = None
    salary: Optional[int] = None
    notes: Optional[str] = None