from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm.session import Session

from app.sql import schemas
from ..sql import crud
from ..dependencies import get_db, valid_tag

router = APIRouter(
    prefix="/tags",
    tags=["tags"]
)

@router.get("")
def read_tags(db: Session = Depends(get_db)):
    return crud.get_tags(db)

@router.get("/{tag_id}", response_model=schemas.Tag)
def read_tag(tag: schemas.Tag = Depends(valid_tag)):
    return tag

@router.post("/", response_model=schemas.Tag)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = crud.get_tag_by_name(db, tag.name)
    if db_tag:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag already exists")
    
    return crud.create_tag(db, tag)

@router.patch("/{tag_id}", response_model=schemas.Tag)
def update_tag(tag_id: int, tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = valid_tag(tag_id, db)
    duplicates = crud.get_tags_by_name(db, tag.name)
    if db_tag and len(duplicates) == 0:
        tag.name = tag.name.lower()
        model_tag = schemas.Tag(**db_tag.__dict__)
        updated_data = tag.dict(exclude_unset=True)
        updated_tag = model_tag.copy(update=updated_data)

        return crud.update_tag(db, tag_id, updated_tag)

    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tag already exists")

@router.delete("/{tag_id}")
def delete_tag(tag: schemas.Tag = Depends(valid_tag), db: Session = Depends(get_db)):
    return crud.delete_tag(db, tag.id)
