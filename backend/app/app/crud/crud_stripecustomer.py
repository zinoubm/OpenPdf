from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.stripe_customer import StripeCustomer
from app.schemas.stripecustomer import StripeCustomerCreate, StripeCustomerUpdate


class CRUDStripeCustomer(
    CRUDBase[StripeCustomer, StripeCustomerCreate, StripeCustomerUpdate]
):
    def create_with_user(
        self, db: Session, *, obj_in: StripeCustomerCreate, user_id: int
    ):
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data, user_id=user_id)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_with_user(self, db: Session, user_id: int):
        result = db.query(self.model).filter(StripeCustomer.user_id == user_id).first()
        return result

    def get_with_stripe_customer_id(self, db: Session, stripe_customer_id: str):
        result = (
            db.query(self.model)
            .filter(StripeCustomer.stripe_customer_id == stripe_customer_id)
            .first()
        )
        return result


stripecustomer = CRUDStripeCustomer(StripeCustomer)
