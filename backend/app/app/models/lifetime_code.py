from sqlalchemy import Column, Integer, String, Boolean
from app.db.base_class import Base

class LifetimeCode(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    code = Column(String(255), nullable=False)
    is_used : bool = Column(Boolean(), default=False)
