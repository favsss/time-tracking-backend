from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session
from app.sql import schemas

from ..sql import crud
from ..dependencies import get_db, valid_user

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.get("/", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db)):
    return crud.get_users(db)

@router.get("/{user_id}", response_model=schemas.User)
def get_user(user: schemas.User = Depends(valid_user)):
    return user

@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with username already exists")

    return crud.create_user(db, user)

@router.delete("/{user_id}")
def delete_user(user: schemas.User = Depends(valid_user), db: Session = Depends(get_db)):
    return crud.delete_user(db, user.id)
