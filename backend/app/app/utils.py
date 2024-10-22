from typing import Any, Dict, Optional
from datetime import datetime, timedelta
from pathlib import Path
from app import crud
from fastapi import HTTPException
from app.stripe.limiter import get_user_plan, get_user_limits
from app.core.constants import (
    FEATURES_ENUM,
    LIFETIME_LOAD_AMOUNTS,
    PLANS_ENUM,
    FEATURES_LIMITS_MATRIX,
)
import logging

from app.core.config import settings
from sqlalchemy.orm import Session


from email.message import EmailMessage
from passlib import pwd
import emails
import smtplib

from emails.template import JinjaTemplate
from jose import jwt


def send_email(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
) -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = emails.Message(
        subject=JinjaTemplate(subject_template),
        html=JinjaTemplate(html_template),
        mail_from=(settings.EMAILS_FROM_NAME, settings.EMAILS_FROM_EMAIL),
    )
    smtp_options = {"host": settings.SMTP_HOST, "port": settings.SMTP_PORT}
    if settings.SMTP_TLS:
        smtp_options["tls"] = True
    if settings.SMTP_USER:
        smtp_options["user"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        smtp_options["password"] = settings.SMTP_PASSWORD
    response = message.send(to=email_to, render=environment, smtp=smtp_options)
    logging.info(f"send email result: {response}")


def send_email_future(
    email_to: str,
    subject_template: str = "",
    html_template: str = "",
    environment: Dict[str, Any] = {},
):
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    logging.info("Using the new code for Emails!")
    smtp_host = settings.SMTP_HOST
    smtp_port = settings.SMTP_PORT
    smtp_user = settings.SMTP_USER
    smtp_password = settings.SMTP_PASSWORD
    smtp_from_email = settings.EMAILS_FROM_EMAIL
    text_subtype = "html"

    message = EmailMessage()
    message.set_content(JinjaTemplate(html_template))

    try:
        message["subject"] = JinjaTemplate(subject_template)
        message["from"] = smtp_from_email
        message["to"] = email_to

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.login(smtp_user, smtp_password)
            server.sendmail(smtp_from_email, email_to, message)

    except Exception as e:
        logging.error(e)
        logging.error("Email couldn't be sent!")

    logging.info(f"Email Sent")


def send_test_email(email_to: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Test email"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "test_email.html") as f:
        template_str = f.read()
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={"project_name": settings.PROJECT_NAME, "email": email_to},
    )


def send_reset_password_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Password recovery for user {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "reset_password.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    link = f"{server_host}/reset-password?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def send_new_account_email(email_to: str, username: str, password: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - New account for user {username}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "new_account.html") as f:
        template_str = f.read()
    link = settings.SERVER_HOST
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": username,
            "password": password,
            "email": email_to,
            "link": link,
        },
    )


def send_verification_email(email_to: str, email: str, token: str) -> None:
    project_name = settings.PROJECT_NAME
    subject = f"{project_name} - Verification Request for {email}"
    with open(Path(settings.EMAIL_TEMPLATES_DIR) / "verify_email.html") as f:
        template_str = f.read()
    server_host = settings.SERVER_HOST
    # change this
    link = f"{server_host}/api/v1/users/verify?token={token}"
    send_email(
        email_to=email_to,
        subject_template=subject,
        html_template=template_str,
        environment={
            "project_name": settings.PROJECT_NAME,
            "username": email,
            "email": email_to,
            "valid_hours": settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS,
            "link": link,
        },
    )


def generate_password_reset_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_password_reset_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["email"]
    except jwt.JWTError:
        return None


def generate_email_verification_token(email: str) -> str:
    delta = timedelta(hours=settings.EMAIL_RESET_TOKEN_EXPIRE_HOURS)
    now = datetime.utcnow()
    expires = now + delta
    exp = expires.timestamp()
    encoded_jwt = jwt.encode(
        {"exp": exp, "nbf": now, "sub": email},
        settings.SECRET_KEY,
        algorithm="HS256",
    )
    return encoded_jwt


def verify_email_verification_token(token: str) -> Optional[str]:
    try:
        decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return decoded_token["sub"]
    except jwt.JWTError:
        return None


def generate_password():
    return pwd.genword()


def limiter(
    db: Session,
    user_id: int,
    feature: str,
):
    # there's 2 types of quotas, monthly and lifetime.
    # first the limiter will check if they have remaining montly quotas
    # if yes increment usage and continue
    # if no
    # limiter will check if they have remaining lifetime quotas
    # if yes decrement track and continue
    # if no raise 402 error

    user_plan, plan_status = get_user_plan(db=db, user_id=user_id)
    if plan_status != "ACTIVE":
        raise HTTPException(
            status_code=402,
            detail=f"Your plan ({user_plan}) Is non active!",
        )

    user_limits = get_user_limits(user_plan)
    usage = crud.user.get_usage(db=db, user_id=user_id)

    if usage[feature] + 1 <= user_limits[feature]:
        crud.user.increment_usage(db=db, user_id=user_id, feature=feature)
        return

    track = crud.user.get_lifetime_track(db=db, user_id=user_id)

    if track[feature] > 0:
        crud.user.decrement_lifetime_track(db=db, user_id=user_id, feature=feature)
        return

    raise HTTPException(
        status_code=402,
        detail=f"Max {feature} limit exeeded for the {user_plan} plan!",
    )
