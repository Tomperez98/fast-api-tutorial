from src.schemas.request import request_post
from datetime import datetime


class CreatedPost(request_post.Post):
    class Config:
        orm_mode = True


class ExistingPost(request_post.Post):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
