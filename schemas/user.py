from typing import Optional
from pydantic import BaseModel, Field


class User(BaseModel):
    id: Optional[str] | None = None
    name: str
    email: str
    password: str
