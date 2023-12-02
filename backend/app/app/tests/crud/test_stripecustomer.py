from sqlalchemy.orm import Session

from app import crud
from app.schemas.stripecustomer import StripeCustomerCreate, StripeCustomerUpdate
from app.tests.utils.user import create_random_user
from app.tests.utils.utils import random_lower_string


def test_create_stripe_customer(db: Session) -> None:
    stripe_customer_id = random_lower_string()
    stripe_subscription_id = random_lower_string()
    stripe_customer_in = StripeCustomerCreate(
        stripe_customer_id=stripe_customer_id, 
        stripe_subscription_id=stripe_subscription_id
    )

    user = create_random_user(db)

    stripe_customer = crud.stripecustomer.create_with_user(db, obj_in=stripe_customer_in, user_id=user.id)

    assert stripe_customer.stripe_customer_id == stripe_customer_id
    assert stripe_customer.stripe_subscription_id == stripe_subscription_id

def test_get_stripe_customer_with_user_id(db: Session) -> None:
    stripe_customer_id = random_lower_string()
    stripe_subscription_id = random_lower_string()
    stripe_customer_in = StripeCustomerCreate(
        stripe_customer_id=stripe_customer_id, 
        stripe_subscription_id=stripe_subscription_id
    )

    user = create_random_user(db)

    stripe_customer = crud.stripecustomer.create_with_user(db, obj_in=stripe_customer_in, user_id=user.id)
    db_stripe_customer = crud.stripecustomer.get_with_user(db, user_id=user.id)
    
    assert stripe_customer.id == db_stripe_customer.id
    assert stripe_customer.stripe_customer_id == db_stripe_customer.stripe_customer_id
    assert stripe_customer.stripe_subscription_id == db_stripe_customer.stripe_subscription_id


    


