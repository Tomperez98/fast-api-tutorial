import pydantic


# TODO: If data required to create_access_token changes, each
# individual attribute has to be added to the class
class TokenData(pydantic.BaseModel):
    user_id: str
