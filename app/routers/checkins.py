from fastapi import APIRouter, Depends
from app.sql import schemas
from typing import List
from sqlalchemy.orm.session import Session

from ..dependencies import get_db, get_current_user, valid_checkin
from ..sql import crud


router = APIRouter(
    prefix="/checkins",
    tags=["checkins"]
)

@router.get("", response_model=List[schemas.Checkin])
def get_checkins(user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.get_checkins(db, user.id)

@router.get("/{checkin_id}", response_model=schemas.Checkin)
def get_checkin(checkin: schemas.Checkin = Depends(valid_checkin)):
    return checkin