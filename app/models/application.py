from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import UniqueConstraint

from app.core.database import Base


class Application(Base):
    __tablename__ = "applications"

    # Global primary key
    id = Column(Integer, primary_key=True, index=True)
    
    user_app_id = Column(Integer, nullable=False)

    company = Column(String, nullable=False)
    role = Column(String, nullable=False)

    status = Column(
        String,
        default="Applied"
    )

    location = Column(String, nullable=True)

    salary = Column(Integer, nullable=True)

    notes = Column(String, nullable=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    __table_args__ = (
        UniqueConstraint('user_id', 'user_app_id', name='uq_user_app_per_user'),
    )