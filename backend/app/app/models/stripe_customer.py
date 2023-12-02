from sqlalchemy import Column, Integer, String, ForeignKey
from app.db.base_class import Base

class StripeCustomer(Base):
    id: int = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    stripe_customer_id = Column(String(255), nullable=False)
    stripe_subscription_id = Column(String(255), nullable=False)
