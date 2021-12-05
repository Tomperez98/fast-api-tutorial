import pydantic


class NoPasswordUser(pydantic.BaseModel):
    # TODO: This EmailStr pydantic class doen't validate email con tildes.
    # We have to implement our own validator
    email: pydantic.EmailStr


class User(NoPasswordUser):
    password: str
