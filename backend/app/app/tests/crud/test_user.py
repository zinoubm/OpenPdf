from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import crud
from app.core.security import verify_password
from app.schemas.user import UserCreate, UserUpdate
from app.tests.utils.utils import random_email, random_lower_string

from app.core.constants import FEATURES_ENUM


def test_create_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    assert user.email == email
    assert hasattr(user, "hashed_password")


def test_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    authenticated_user = crud.user.authenticate(db, email=email, password=password)
    assert authenticated_user
    assert user.email == authenticated_user.email


def test_not_authenticate_user(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user = crud.user.authenticate(db, email=email, password=password)
    assert user is None


def test_check_if_user_is_active(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active is True


def test_check_if_user_is_active_inactive(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, disabled=True)
    user = crud.user.create(db, obj_in=user_in)
    is_active = crud.user.is_active(user)
    assert is_active


def test_check_if_user_is_superuser(db: Session) -> None:
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = crud.user.create(db, obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is True


def test_check_if_user_is_superuser_normal_user(db: Session) -> None:
    username = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=username, password=password)
    user = crud.user.create(db, obj_in=user_in)
    is_superuser = crud.user.is_superuser(user)
    assert is_superuser is False


def test_get_user(db: Session) -> None:
    password = random_lower_string()
    username = random_email()
    user_in = UserCreate(email=username, password=password, is_superuser=True)
    user = crud.user.create(db, obj_in=user_in)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert jsonable_encoder(user) == jsonable_encoder(user_2)


def test_update_user(db: Session) -> None:
    password = random_lower_string()
    email = random_email()
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    user = crud.user.create(db, obj_in=user_in)
    new_password = random_lower_string()
    user_in_update = UserUpdate(password=new_password, is_superuser=True)
    crud.user.update(db, db_obj=user, obj_in=user_in_update)
    user_2 = crud.user.get(db, id=user.id)
    assert user_2
    assert user.email == user_2.email
    assert verify_password(new_password, user_2.hashed_password)


def test_get_usage(db: Session):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)

    usage = crud.user.get_usage(db=db, user_id=user.id)
    assert usage[FEATURES_ENUM.UPLOADS] == 0
    assert usage[FEATURES_ENUM.QUERIES] == 0


def test_increment_usage(db: Session):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)

    usage = crud.user.get_usage(db=db, user_id=user.id)
    assert usage[FEATURES_ENUM.UPLOADS] == 0
    assert usage[FEATURES_ENUM.QUERIES] == 0

    crud.user.increment_usage(db=db, user_id=user.id, feature=FEATURES_ENUM.UPLOADS)
    usage = crud.user.get_usage(db=db, user_id=user.id)
    assert usage[FEATURES_ENUM.UPLOADS] == 1
    assert usage[FEATURES_ENUM.QUERIES] == 0

    crud.user.increment_usage(db=db, user_id=user.id, feature=FEATURES_ENUM.QUERIES)
    usage = crud.user.get_usage(db=db, user_id=user.id)
    assert usage[FEATURES_ENUM.UPLOADS] == 1
    assert usage[FEATURES_ENUM.QUERIES] == 1


def test_reset_usage(db: Session):
    email = random_email()
    password = random_lower_string()
    user_in = UserCreate(email=email, password=password)
    user = crud.user.create(db, obj_in=user_in)

    crud.user.increment_usage(
        db=db, user_id=user.id, feature=FEATURES_ENUM.QUERIES, amount=5
    )

    crud.user.increment_usage(
        db=db, user_id=user.id, feature=FEATURES_ENUM.UPLOADS, amount=3
    )

    usage = crud.user.get_usage(db=db, user_id=user.id)
    assert usage[FEATURES_ENUM.UPLOADS] != 0
    assert usage[FEATURES_ENUM.QUERIES] != 0

    crud.user.reset_usage(db=db, user_id=user.id)
    usage = crud.user.get_usage(db=db, user_id=user.id)
    assert usage[FEATURES_ENUM.UPLOADS] == 0
    assert usage[FEATURES_ENUM.QUERIES] == 0


def test_reset_usage_all(db: Session):
    email_1 = random_email()
    password_1 = random_lower_string()
    user_in_1 = UserCreate(email=email_1, password=password_1)
    user_1 = crud.user.create(db, obj_in=user_in_1)

    email_2 = random_email()
    password_2 = random_lower_string()
    user_in_2 = UserCreate(email=email_2, password=password_2)
    user_2 = crud.user.create(db, obj_in=user_in_2)

    email_3 = random_email()
    password_3 = random_lower_string()
    user_in_3 = UserCreate(email=email_3, password=password_3)
    user_3 = crud.user.create(db, obj_in=user_in_3)

    crud.user.increment_usage(
        db=db, user_id=user_1.id, feature=FEATURES_ENUM.QUERIES, amount=5
    )

    crud.user.increment_usage(
        db=db, user_id=user_2.id, feature=FEATURES_ENUM.UPLOADS, amount=3
    )

    crud.user.increment_usage(
        db=db, user_id=user_3.id, feature=FEATURES_ENUM.UPLOADS, amount=12
    )

    crud.user.reset_usage_all(db=db)

    usage = crud.user.get_usage(db=db, user_id=user_1.id)
    assert usage[FEATURES_ENUM.UPLOADS] == 0
    assert usage[FEATURES_ENUM.QUERIES] == 0

    usage = crud.user.get_usage(db=db, user_id=user_2.id)
    assert usage[FEATURES_ENUM.UPLOADS] == 0
    assert usage[FEATURES_ENUM.QUERIES] == 0

    usage = crud.user.get_usage(db=db, user_id=user_3.id)
    assert usage[FEATURES_ENUM.UPLOADS] == 0
    assert usage[FEATURES_ENUM.QUERIES] == 0
