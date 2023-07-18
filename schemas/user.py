from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[str] = Field(None)
    name: Optional[str] = Field(None)
    email: str
    password: str
