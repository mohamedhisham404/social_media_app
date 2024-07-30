from pydantic import BaseModel
from datetime import datetime
from .users import UserResponse
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse
    votes: int = 0

    class Config:
        orm_mode = True