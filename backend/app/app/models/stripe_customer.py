from sqlalchemy import Column, Integer, String
from app.db.base_class import Base

class StripeCustomer(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    stripeCustomerId = Column(String(255), nullable=False)
    stripeSubscriptionId = Column(String(255), nullable=False)
