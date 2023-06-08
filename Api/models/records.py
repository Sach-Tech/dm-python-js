from typing import Optional
from pydantic import BaseModel,Field


# Record models

class Record(BaseModel):
    longitude: str = Field(min_length=1, max_length=16)
    latitude: str = Field(min_length=1, max_length=16)
    imageUrl: str
    created_at : str
    updated_at : str