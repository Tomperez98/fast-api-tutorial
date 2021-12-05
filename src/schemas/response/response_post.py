from src.schemas.request import request_post
from src.schemas.response import response_user
from datetime import datetime


class CreatedPost(request_post.Post):
    class Config:
        orm_mode = True


class ExistingPost(request_post.Post):
    id: int
    created_at: datetime
    owner: response_user.ExistingUser

    class Config:
        orm_mode = True
