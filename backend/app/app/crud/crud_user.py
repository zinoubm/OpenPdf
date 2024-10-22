from typing import Any, Dict, Optional, Union

from sqlalchemy.orm import Session

from app.core.security import get_password_hash, verify_password
from app.crud.base import CRUDBase
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate

from app.core.constants import FEATURES_ENUM, LIFETIME_LOAD_AMOUNTS


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_superuser=obj_in.is_superuser,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: User, obj_in: Union[UserUpdate, Dict[str, Any]]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        if update_data.get("password", None):
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            update_data["hashed_password"] = hashed_password
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def is_active(self, user: User) -> bool:
        return user.is_active

    def is_verified(self, user: User) -> bool:
        return user.is_verified

    def verify(self, db: Session, user: User):
        user.is_verified = True
        db.add(user)
        db.commit()
        return user

    def is_superuser(self, user: User) -> bool:
        return user.is_superuser

    def get_usage(self, db: Session, user_id):
        user = self.get(db=db, id=user_id)
        return {
            FEATURES_ENUM.UPLOADS: user.uploads_counter,
            FEATURES_ENUM.QUERIES: user.queries_counter,
        }

    def increment_usage(self, db: Session, user_id, feature, amount=1):
        user = self.get(db=db, id=user_id)

        if feature == FEATURES_ENUM.UPLOADS:
            user.uploads_counter += amount
            db.add(user)
            db.commit()

            return user

        if feature == FEATURES_ENUM.QUERIES:
            user.queries_counter += amount
            db.add(user)
            db.commit()

            return user

        raise Exception("Non valid feature")

    def reset_usage(self, db: Session, user_id):
        user = self.get(db=db, id=user_id)
        user.uploads_counter = 0
        user.queries_counter = 0
        db.add(user)
        db.commit()

        return user

    def reset_usage_all(self, db: Session):
        db.query(User).update({User.uploads_counter: 0, User.queries_counter: 0})
        db.commit()

        return True
    
    def get_lifetime_track(self, db: Session, user_id):
        user = self.get(db=db, id=user_id)
        return {
            FEATURES_ENUM.UPLOADS: user.lifetime_uploads_counter,
            FEATURES_ENUM.QUERIES: user.lifetime_queries_counter,
        }

    def load_lifetime_track(self, db: Session, user_id):
        user = self.get(db=db, id=user_id)
        current_lifetime_uploads_counter = user.lifetime_uploads_counter
        current_lifetime_queries_counter = user.lifetime_queries_counter
        user.lifetime_uploads_counter = current_lifetime_uploads_counter + LIFETIME_LOAD_AMOUNTS[FEATURES_ENUM.UPLOADS]
        user.lifetime_queries_counter = current_lifetime_queries_counter + LIFETIME_LOAD_AMOUNTS[FEATURES_ENUM.QUERIES]
        db.add(user)
        db.commit()

        return user

    def decrement_lifetime_track(self, db: Session, user_id, feature, amount=1):
        user = self.get(db=db, id=user_id)

        if feature == FEATURES_ENUM.UPLOADS:
            user.lifetime_uploads_counter -= amount
            db.add(user)
            db.commit()

            return user

        if feature == FEATURES_ENUM.QUERIES:
            user.lifetime_queries_counter -= amount
            db.add(user)
            db.commit()

            return user

        raise Exception("Non valid feature")

user = CRUDUser(User)
