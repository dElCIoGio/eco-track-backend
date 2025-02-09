from datetime import datetime

from pydantic import BaseModel, Field

from app.schema.identificator import PyObjectId
from app.utils.utils import get_time_now


class Display(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    created_at: datetime = Field(default_factory=get_time_now)