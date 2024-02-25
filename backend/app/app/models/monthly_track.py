from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base

class MonthlyTrack(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    uploads_counter = Column(Integer, default=0, nullable=False)
    queries_counter = Column(Integer, default=0, nullable=False) 