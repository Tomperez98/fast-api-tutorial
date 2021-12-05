from src.schemas.request import request_user
from datetime import datetime


class CreatedUser(request_user.NoPasswordUser):
    id: int

    class Config:
        orm_mode = True


class ExistingUser(request_user.NoPasswordUser):
    id: int
    email: str
    created_at: datetime

    class Config:
        orm_mode = True
