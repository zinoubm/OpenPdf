from fastapi import APIRouter, Depends
import stripe
from app.core.config import settings
from app import models
from app.api import deps


router = APIRouter()
stripe.api_key = settings.STRIPE_SECRET_KEY


@router.get("/upgrade-key")
def get_publishable_key(
    current_user: models.User = Depends(deps.get_current_active_user),
):
    return {"key": settings.STRIPE_PUBLISHABLE_KEY}


@router.get("/create-checkout-session")
def create_checkout_session(
    plan: str,
    current_user: models.User = Depends(deps.get_current_active_user),
):
    domain = settings.FRONTEND_DOMAIN
    try:
        checkout_session = stripe.checkout.Session.create(
            client_reference_id=current_user.id,
            success_url="http://" + domain + "/success?session_id={CHECKOUT_SESSION_ID}",
            cancel_url="http://" + domain + "/cancel",
            payment_method_types=["card"],
            mode="subscription",
            line_items=[
                {
                    "price": stripe_keys["price_id"],
                    "quantity": 1,
                }
            ]
        )
        return {"sessionId": checkout_session["id"]}
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail="Couldn't create checkout session, Please retry again!",
        )
