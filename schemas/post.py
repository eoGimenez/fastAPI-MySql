from typing import Optional
from pydantic import BaseModel, Field


class Post(BaseModel):
    id: Optional[str] = Field(None)
    place: str
    comment: str
    image: Optional[str] = Field(None)
    author: Optional[str] = Field(None)
