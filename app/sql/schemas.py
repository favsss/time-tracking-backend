from datetime import datetime, timedelta
from typing import Optional, Union
from pydantic import BaseModel
from enum import Enum

class TagBase(BaseModel):
    name: str 

class TagCreate(TagBase):
    pass 

class Tag(TagBase):
    id: int 

    class Config:
        orm_mode = True

class UserType(str, Enum):
    ADMIN = "Admin"
    REGULAR = "Regular"

class UserBase(BaseModel):
    username: str 
    type: Optional[UserType] = UserType.REGULAR

class UserCreate(UserBase):
    password: str 

class User(UserBase):
    id: int 

    class Config:
        orm_mode = True

class CheckinBase(BaseModel):
    hours: float
    activity: str

class CheckinCreate(CheckinBase):
    tag: str

class Checkin(CheckinBase):
    id: int 
    user_id: int 
    tag_id: int 
    creation_date: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str 
    token_type: str
    

class TokenData(BaseModel):
    username: Union[str, None] = None