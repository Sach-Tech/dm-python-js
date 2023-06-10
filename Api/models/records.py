from typing import Optional
from pydantic import BaseModel,Field


# Record models

class Record(BaseModel):

    longitude: str = Field(min_length=0, max_length=50)
    latitude: str = Field(min_length=0, max_length=50)
    altitude: str = Field(min_length=0, max_length=50)
    has_tag: str
    imageUrl: str
    created_at : str
    updated_at : str

    