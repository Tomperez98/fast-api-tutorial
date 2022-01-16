from app.schemas.request import request_post
from app.schemas.response import response_user
import datetime


class CreatedPost(request_post.Post):
    class Config:
        orm_mode = True


class ExistingPost(request_post.Post):
    id: int
    created_at: datetime.datetime
    owner: response_user.ExistingUser

    class Config:
        orm_mode = True
