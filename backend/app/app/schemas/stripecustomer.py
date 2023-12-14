from pydantic import BaseModel

class StripeCustomerBase(BaseModel):
    stripe_customer_id: str
    stripe_subscription_id: str

class StripeCustomerCreate(StripeCustomerBase):
    pass

class StripeCustomerUpdate(StripeCustomerBase):
    pass
