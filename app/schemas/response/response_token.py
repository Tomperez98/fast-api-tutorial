import pydantic


class PlainToken(pydantic.BaseModel):
    access_token: str
    token_type: str

    class Config:
        orm_mode = True
