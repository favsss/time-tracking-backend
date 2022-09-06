from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, text
from sqlalchemy.orm import relationship
from .database import Base

metadata = Base.metadata

class Tag(Base):
    __tablename__ = 'tags'

    id = Column(Integer, primary_key=True, server_default=text("nextval('tags_id_seq'::regclass)"))
    name = Column(String(255))


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, server_default=text("nextval('users_id_seq'::regclass)"))
    username = Column(String(255))
    password = Column(String(255))
    type = Column(String(255))


class Checkin(Base):
    __tablename__ = 'checkins'

    id = Column(Integer, primary_key=True, server_default=text("nextval('checkins_id_seq'::regclass)"))
    user_id = Column(ForeignKey('users.id'))
    tag_id = Column(ForeignKey('tags.id'))
    activity = Column(String(255))
    hours = Column(Float(53))
    creation_date = Column(DateTime, nullable=False, server_default=text("CURRENT_TIMESTAMP"))

    tag = relationship('Tag')
    user = relationship('User')