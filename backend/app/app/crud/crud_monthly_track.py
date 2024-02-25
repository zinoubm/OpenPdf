from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.monthly_track import MonthlyTrack
from app.schemas.monthly_track import MonthlyTrackCreate, MonthlyTrackUpdate


class CRUDMonthlyTrack(CRUDBase[MonthlyTrack, MonthlyTrackCreate, MonthlyTrackUpdate]):
    pass

monthly_track = CRUDMonthlyTrack(MonthlyTrack) 
