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

@router.post("", response_model=schemas.Checkin)
def create_checkin(checkin: schemas.CheckinCreate, user: schemas.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return crud.create_checkin(db, user.id, checkin)

@router.delete("/{checkin_id}")
def delete_checkin(checkin: schemas.Checkin = Depends(valid_checkin), db: Session = Depends(get_db)):
    return crud.delete_checkin(db, checkin.id)