from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from app.sql import schemas
from ..sql import crud
from ..dependencies import get_db

router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)

@router.get("/")
def read_tags(db: Session = Depends(get_db)):
    return crud.get_tags(db)

@router.get("/{tag_id}", response_model=schemas.Tag)
def read_tag(tag_id: int, db: Session = Depends(get_db)):
    db_tag = crud.get_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Tag not found")

    return db_tag

@router.post("/", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = crud.get_tag_by_name(db, tag.name)
    print(db_tag)
    if db_tag:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag already exists")
    
    return crud.create_tag(db, tag)
