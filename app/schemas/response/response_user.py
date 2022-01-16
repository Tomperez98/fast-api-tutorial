from app.schemas.request import request_user
import datetime


class CreatedUser(request_user.NoPasswordUser):
    id: int

    class Config:
        orm_mode = True


class ExistingUser(request_user.NoPasswordUser):
    id: int
    email: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True
