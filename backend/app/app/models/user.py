from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import relationship, Mapped

from app.db.base_class import Base

if TYPE_CHECKING:
    from .document import Document  # noqa: F401


class User(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email: str = Column(String, unique=True, index=True, nullable=False)
    hashed_password: str = Column(String, nullable=False)
    google_account_id: str = Column(String, unique=True, nullable=True)
    is_verified: bool = Column(Boolean(), default=False)
    is_active: bool = Column(Boolean(), default=True)
    is_superuser: bool = Column(Boolean(), default=False)
    documents: Mapped["Document"] = relationship("Document", back_populates="user")
