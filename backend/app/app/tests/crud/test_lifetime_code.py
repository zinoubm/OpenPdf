import pytest
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string
from app.core.constants import (
    FEATURES_ENUM,
    LIFETIME_LOAD_AMOUNTS,
    PLANS_ENUM,
    FEATURES_LIMITS_MATRIX,
)
from unittest.mock import patch
from app.stripe.limiter import get_user_plan
from app.utils import limiter

from app import crud


@pytest.mark.skip(reason="Test case is disabled for now")
def test_check_code(db: Session):
    # non valid code
    result = crud.lifetime_code.check_code(db=db, code="hello")
    assert result == None

    # valid non used code
    result = crud.lifetime_code.check_code(db=db, code="test_unused_code")
    assert result == False

    # valid used code
    result = crud.lifetime_code.check_code(db=db, code="test_used_code")
    assert result == True


def test_redeem_code(db: Session):
    code = crud.lifetime_code.redeem_code(db=db, code="test_unused_code")
    result = crud.lifetime_code.check_code(db=db, code="test_unused_code")
    assert result == True


def test_get_lifetime_track(db: Session):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    track = crud.user.get_lifetime_track(db, user.id)

    assert track[FEATURES_ENUM.UPLOADS] == 0
    assert track[FEATURES_ENUM.QUERIES] == 0


def test_load_lifetime_track(db: Session):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    crud.user.load_lifetime_track(db, user.id)
    track = crud.user.get_lifetime_track(db, user.id)

    assert track[FEATURES_ENUM.UPLOADS] == LIFETIME_LOAD_AMOUNTS[FEATURES_ENUM.UPLOADS]
    assert track[FEATURES_ENUM.QUERIES] == LIFETIME_LOAD_AMOUNTS[FEATURES_ENUM.QUERIES]

    crud.user.load_lifetime_track(db, user.id)
    track = crud.user.get_lifetime_track(db, user.id)

    assert track[FEATURES_ENUM.UPLOADS] == (int)(
        LIFETIME_LOAD_AMOUNTS[FEATURES_ENUM.UPLOADS] * 2
    )
    assert track[FEATURES_ENUM.QUERIES] == (int)(
        LIFETIME_LOAD_AMOUNTS[FEATURES_ENUM.QUERIES] * 2
    )


def test_decrement_lifetime_track(db: Session):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    crud.user.load_lifetime_track(db, user.id)
    track = crud.user.get_lifetime_track(db, user.id)
    assert track[FEATURES_ENUM.UPLOADS] == LIFETIME_LOAD_AMOUNTS[FEATURES_ENUM.UPLOADS]
    assert track[FEATURES_ENUM.QUERIES] == LIFETIME_LOAD_AMOUNTS[FEATURES_ENUM.QUERIES]

    crud.user.decrement_lifetime_track(
        db=db, user_id=user.id, feature=FEATURES_ENUM.UPLOADS
    )
    track = crud.user.get_lifetime_track(db, user.id)
    assert track[FEATURES_ENUM.UPLOADS] == (int)(
        LIFETIME_LOAD_AMOUNTS[FEATURES_ENUM.UPLOADS] - 1
    )
    assert track[FEATURES_ENUM.QUERIES] == LIFETIME_LOAD_AMOUNTS[FEATURES_ENUM.QUERIES]

    crud.user.decrement_lifetime_track(
        db=db, user_id=user.id, feature=FEATURES_ENUM.QUERIES
    )
    track = crud.user.get_lifetime_track(db, user.id)
    assert track[FEATURES_ENUM.UPLOADS] == (int)(
        LIFETIME_LOAD_AMOUNTS[FEATURES_ENUM.UPLOADS] - 1
    )
    assert track[FEATURES_ENUM.QUERIES] == (int)(
        LIFETIME_LOAD_AMOUNTS[FEATURES_ENUM.QUERIES] - 1
    )


# there's 2 types of quotas, monthly and lifetime.
# first the limiter will check if they have remaining montly quotas
# if yes increment usage and continue
# if no
# limiter will check if they have remaining lifetime quotas
# if yes decrement track and continue
# if no raise 402 error


# def test_limiter_non_active_plan(db: Session):
#     feature = FEATURES_ENUM.UPLOADS
#     email = random_email()
#     password = random_lower_string()
#     user_in = UserCreate(email=email, password=password)
#     user = crud.user.create(db, obj_in=user_in)

#     user.uploads_counter = FEATURES_LIMITS_MATRIX[PLANS_ENUM.FREE][feature]
#     user.lifetime_uploads_counter = 0

#     with pytest.raises(HTTPException):
#         limiter(db=db, user_id=user.id, feature=feature)


def test_limiter_no_monthly_no_lifetime_uploads(db: Session):
    feature = FEATURES_ENUM.UPLOADS
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)

    user.uploads_counter = FEATURES_LIMITS_MATRIX[PLANS_ENUM.FREE][feature]
    user.lifetime_uploads_counter = 0

    with pytest.raises(HTTPException):
        limiter(db=db, user_id=user.id, feature=feature)


def test_limiter_with_monthly_no_lifetime_uploads(db: Session):
    feature = FEATURES_ENUM.UPLOADS
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)

    user.uploads_counter = FEATURES_LIMITS_MATRIX[PLANS_ENUM.FREE][feature] - 1
    user.lifetime_uploads_counter = 0
    limiter(db=db, user_id=user.id, feature=feature)

    db_user = crud.user.get(db=db, id=user.id)

    assert db_user.uploads_counter == FEATURES_LIMITS_MATRIX[PLANS_ENUM.FREE][feature]


def test_limiter_no_monthly_with_lifetime_uploads(db: Session):
    feature = FEATURES_ENUM.UPLOADS
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)

    user.uploads_counter = FEATURES_LIMITS_MATRIX[PLANS_ENUM.FREE][feature]
    user.lifetime_uploads_counter = 1
    limiter(db=db, user_id=user.id, feature=feature)

    db_user = crud.user.get(db=db, id=user.id)

    assert db_user.lifetime_uploads_counter == 0


def test_limiter_no_monthly_no_lifetime_queries(db: Session):
    feature = FEATURES_ENUM.QUERIES
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)

    user.queries_counter = FEATURES_LIMITS_MATRIX[PLANS_ENUM.FREE][feature]
    user.lifetime_queries_counter = 0

    with pytest.raises(HTTPException):
        limiter(db=db, user_id=user.id, feature=feature)


def test_limiter_with_monthly_no_lifetime_queries(db: Session):
    feature = FEATURES_ENUM.QUERIES
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)

    user.queries_counter = FEATURES_LIMITS_MATRIX[PLANS_ENUM.FREE][feature] - 1
    user.lifetime_queries_counter = 0
    limiter(db=db, user_id=user.id, feature=feature)

    db_user = crud.user.get(db=db, id=user.id)

    assert db_user.queries_counter == FEATURES_LIMITS_MATRIX[PLANS_ENUM.FREE][feature]


def test_limiter_no_monthly_with_lifetime_queries(db: Session):
    feature = FEATURES_ENUM.QUERIES
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)

    user.queries_counter = FEATURES_LIMITS_MATRIX[PLANS_ENUM.FREE][feature]
    user.lifetime_queries_counter = 1
    limiter(db=db, user_id=user.id, feature=feature)

    db_user = crud.user.get(db=db, id=user.id)

    assert db_user.lifetime_queries_counter == 0


def test_limiter_with_monthly_with_lifetime(db: Session):
    pass
