from typing import TYPE_CHECKING
from datetime import datetime

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from sqlalchemy.sql.functions import func
from sqlalchemy.sql.sqltypes import DateTime

from app.db.base_class import Base

if TYPE_CHECKING:
    from .user import User  # noqa: F401


# class Document(Base):
#     id: int = Column(Integer, primary_key=True, index=True)
#     title = Column(String, index=True)
#     description = Column(String, index=True)
#     owner_id = Column(Integer, ForeignKey("user.id"))
#     owner: "User" = relationship("User", back_populates="documents")


class Document(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    preview = Column(String, nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    owner_id = Column(Integer, ForeignKey("user.id"))
    owner: Mapped["User"] = relationship("User", back_populates="documents")
