from .sql import models, schemas, crud
from .sql.database import SessionLocal, engine
from sqlalchemy.orm.session import Session
from fastapi import Depends, HTTPException, status

models.Base.metadata.create_all(engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def valid_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = crud.get_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

    return db_tag

def valid_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return db_user