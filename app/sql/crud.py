from pyexpat import model
from tabnanny import check
from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext


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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate(db: Session, username: str, password: str):
    db_user = get_user_by_username(db, username)
    if db_user and verify_password(password, db_user.password):
        return db_user 
    return False

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        username=user.username,
        password=get_password_hash(user.password),
        type=user.type
    )

    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users(db: Session):
    return db.query(models.User).all()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def delete_user(db: Session, user_id: int):
    db.query(models.User).filter(models.User.id == user_id).delete()
    db.commit()
    return { "success" : True }

def get_checkins(db: Session, user_id: int):
    query = db.query(models.Checkin, models.Tag).filter(models.Checkin.tag_id == models.Tag.id).filter(models.Checkin.user_id == user_id).all()
    checkins = []
    
    for c, t in query:
        checkins.append({
            "id" : c.id,
            "user_id" : c.user_id,
            "tag_id" : c.tag_id,
            "tag" : t.name,
            "hours" : c.hours,
            "activity" : c.activity,
            "creation_date" : c.creation_date
        })

    return checkins

def get_checkin(db: Session, checkin_id: int):
    db_checkin = db.query(models.Checkin).filter(models.Checkin.id == checkin_id).first()
    if db_checkin is None:
        return None

    # needed to complete the data
    db_tag = get_tag(db, db_checkin.tag_id)
    return {
        "id" : db_checkin.__dict__["id"],
        "user_id" : db_checkin.__dict__["user_id"],
        "tag_id" : db_checkin.__dict__["tag_id"],
        "tag" : db_tag.__dict__["name"],
        "activity" : db_checkin.__dict__["activity"],
        "hours" : db_checkin.__dict__["hours"],
        "creation_date" : db_checkin.__dict__["creation_date"]
    }

def create_checkin(db: Session, user_id: int, checkin: schemas.CheckinCreate):
    tag = checkin.tag.lower()
    db_tag = get_tag_by_name(db, tag)
    tag_id = None
    if db_tag is None:
        new_db_tag = create_tag(db, schemas.TagCreate(name=tag))
        tag_id = new_db_tag.id
    else:
        tag_id = db_tag.id

    db_checkin = models.Checkin(
        user_id=user_id,
        tag_id=tag_id,
        activity=checkin.activity,
        hours=checkin.hours
    )

    db.add(db_checkin)
    db.commit()
    db.refresh(db_checkin)

    db_tag = db.query(models.Tag).filter(models.Tag.id == db_checkin.tag_id).first()

    return {
        "id" : db_checkin.id,
        "user_id" : db_checkin.user_id,
        "tag_id" : db_checkin.tag_id,
        "tag" : db_tag.__dict__["name"],
        "activity" : db_checkin.activity,
        "hours" : db_checkin.hours,
        "creation_date" : db_checkin.creation_date
    }

def delete_checkin(db: Session, checkin_id: int):
    db.query(models.Checkin).filter(models.Checkin.id == checkin_id).delete()
    db.commit()
    return { "success" : True }

