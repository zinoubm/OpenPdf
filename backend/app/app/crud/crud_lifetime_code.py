from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.lifetime_code import LifetimeCode
from app.schemas.lifetime_code import LifetimeCodeCreate, LifetimeCodeUpdate


class CRUDLifetimeCode(CRUDBase[LifetimeCode, LifetimeCodeCreate, LifetimeCodeUpdate]):
    def check_code(self, db: Session, code: str):
        code = db.query(self.model).filter(LifetimeCode.code == code).first()
        if not code:
            return None

        return code.is_used

    def redeem_code(self, db: Session, code: str):
        code = db.query(self.model).filter(LifetimeCode.code == code).first()
        code.is_used = True

        db.add(code)
        db.commit()

        return code

lifetime_code = CRUDLifetimeCode(LifetimeCode) 
