import stripe
from app import crud
from app.core.constants import PLANS_ENUM, FEATURES_LIMITS_MATRIX


def get_user_plan(db, user_id):
    stripe_customer = crud.stripecustomer.get_with_user(db=db, user_id=user_id)

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


# maybe we don't need this
def get_user_subscription_status(user_id):
    pass


def get_user_usage(user_id):
    pass


def increment_user_usage(user_id, feature):
    pass
