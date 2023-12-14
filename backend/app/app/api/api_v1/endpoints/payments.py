from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from typing import Optional
from sqlalchemy.orm import Session

import stripe

from app import crud
from app.schemas.stripecustomer import StripeCustomerCreate
from app.core.config import settings
from app.core.security import verify_password
from app import models
from app.api import deps
from app.stripe.limiter import get_user_plan, get_user_limits


router = APIRouter()
stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/webhook")
async def webhook(request: Request, db: Session = Depends(deps.get_db)):
    payload = await request.body()
    sig_header = request.headers.get("Stripe-Signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_ENDPOINT_SECRET
        )

        if event["type"] == "checkout.session.completed":
            session = event["data"]["object"]
            stripe_customer_id = session["customer"]
            stripe_subscription_id = session["subscription"]
            user_id = session["client_reference_id"]

            stripe_customer = crud.stripecustomer.get_with_user(db=db, user_id=user_id)

            if not stripe_customer:
                stripe_customer_in = StripeCustomerCreate(
                    stripe_customer_id=stripe_customer_id,
                    stripe_subscription_id=stripe_subscription_id,
                )
                stripe_customer = crud.stripecustomer.create_with_user(
                    db,
                    obj_in=stripe_customer_in,
                    user_id=user_id,
                )
            # reset usage for upgraded accounts
            # user = crud.user.reset_usage(db=db, user_id=user_id)


        if event["type"] == "customer.subscription.updated":
            subscription = event["data"]["object"]
            stripe_customer_id = subscription["customer"]
            stripe_customer = crud.stripecustomer.get_with_stripe_customer_id(
                db=db, stripe_customer_id=stripe_customer_id
            )

            user_id = stripe_customer.user_id
            user = crud.user.reset_usage(db=db, user_id=user_id)

    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")

    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid signature")

    return JSONResponse(content={"message": "Success"}, status_code=200)


@router.get("/summary")
def summary(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    user_plan, plan_status = get_user_plan(db=db, user_id=current_user.id)
    user_limits = get_user_limits(user_plan)
    usage = crud.user.get_usage(db=db, user_id=current_user.id)

    return {
        "plan": user_plan,
        "plan_status": plan_status,
        "user_limits": user_limits,
        "usage": usage,
    }


@router.get("/customer-portal")
def customer_portal(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
):
    stripe_customer = crud.stripecustomer.get_with_user(db=db, user_id=current_user.id)

    if stripe_customer:
        portal = stripe.billing_portal.Session.create(
            customer=stripe_customer.stripe_customer_id,
        )

        return {"url": portal.url}

    raise HTTPException(status_code=400, detail="User has no subscriptions")


@router.post("/reset")
def reset_usage(
    secret: str,
    db: Session = Depends(deps.get_db),
):
    if not verify_password(
        plain_password=secret, hashed_password=settings.CRON_JOB_SECRET_KEY
    ):
        raise HTTPException(
            status_code=403, detail="You Don't have the premission requred!"
        )

    crud.user.reset_usage_all(db=db)

    return {"Detail": "success"}
