from msilib import schema
from pyexpat import model
from unicodedata import name
from sqlalchemy.orm import Session
from . import models, schemas

def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first() 

def get_tag_by_name(db: Session, tag_name: str):
    return db.query(models.Tag).filter(models.Tag.name == tag_name.lower()).first() 

def get_tags_by_name(db: Session, tag_name: str):
    return db.query(models.Tag).filter(models.Tag.name == tag_name.lower()).all()

def get_tags(db: Session):
    return db.query(models.Tag).all()

def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(name=tag.name.lower())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)

    return db_tag

def update_tag(db: Session, tag_id: int, tag: schemas.Tag):
    db.query(models.Tag).filter(models.Tag.id == tag_id).update(tag.dict())
    db.commit()
    db_tag = get_tag(db, tag_id)
    return db_tag

def delete_tag(db: Session, tag_id: int):
    db.query(models.Tag).filter(models.Tag.id == tag_id).delete()
    db.commit()
    return { "success" : True }