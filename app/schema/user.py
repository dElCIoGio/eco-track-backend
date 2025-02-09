from datetime import datetime
from typing import Optional
from beanie import Document

from app.schema.display import Display
from pydantic import BaseModel, EmailStr
from bson import ObjectId


class UserBase(BaseModel):
    email: EmailStr
    firebase_uid: str
    actions: Optional[list[str]] = []



class UserCreate(UserBase):
    """
    email: EmailStr
    firebase_uid: str
    """
    pass


class User(UserBase, Display):
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class UserDocument(User, Document):

    class Settings:
        name = "users"