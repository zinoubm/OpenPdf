import stripe
from app import crud
from app.core.constants import PLANS_ENUM, FEATURES_LIMITS_MATRIX


def get_user_plan(db, user_id):
    user = crud.user.get(db=db, id=user_id)
    stripe_customer = crud.stripecustomer.get_with_user(db=db, user_id=user_id)

    if user.is_superuser:
        return PLANS_ENUM.ADMIN, "ACTIVE"

    if stripe_customer:
        subscription = stripe.Subscription.retrieve(
            stripe_customer.stripe_subscription_id
        )
        product = stripe.Product.retrieve(subscription.plan.product)

        if product["name"].upper() == PLANS_ENUM.PRO:
            return PLANS_ENUM.PRO, subscription.status.upper()

        if product["name"].upper() == PLANS_ENUM.PREMIUM:
            return PLANS_ENUM.PREMIUM, subscription.status.upper()

        if product["name"].upper() == PLANS_ENUM.BUSINESS:
            return PLANS_ENUM.BUSINESS, subscription.status.upper()

    return PLANS_ENUM.FREE, "ACTIVE"


def get_user_limits(plan):
    if plan:
        return FEATURES_LIMITS_MATRIX[plan]

    return FEATURES_LIMITS_MATRIX[PLANS_ENUM.FREE]