
from datetime import datetime
from enum import Enum
from typing import get_type_hints, Optional

from beanie import Document

from app.schema.display import Display
from pydantic import BaseModel, create_model
from bson import ObjectId

from app.schema.identificator import PyObjectId


class Category(str, Enum):
    RECYCLING = "reciclagem"
    ENERGY = "energia"
    WATER = "água"
    MOBILITY = "mobilidade"


class SustainabilityActionBase(BaseModel):
    title: str
    description: Optional[str] = ""
    category: Optional[Category] = Category.RECYCLING
    points: Optional[int] = 0
    user_id: str

class SustainabilityActionCreate(SustainabilityActionBase):
    """
    title: str
    user_id: str
    """
    pass


SustainabilityActionUpdate = create_model(
    "SustainabilityActionUpdate",
    **{field: (Optional[typ], None) for field, typ in get_type_hints(SustainabilityActionBase).items()}
)


class SustainabilityAction(SustainabilityActionBase, Display):
    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}


class SustainabilityActionDocument(SustainabilityAction, Document):
    class Settings:
        name = "sustainability actions"

        indexes = [
            [("user_id", 1)]
        ]

