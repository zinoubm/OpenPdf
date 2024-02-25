from typing import List

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.lifetime_track import LifetimeTrack
from app.schemas.lifetime_track import LifetimeTrackCreate, LifetimeTrackUpdate


class CRUDLifetimeTrack(CRUDBase[LifetimeTrack, LifetimeTrackCreate, LifetimeTrackUpdate]):
    pass

lifetime_track = CRUDLifetimeTrack(LifetimeTrack) 
