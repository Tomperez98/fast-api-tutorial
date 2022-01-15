import pydantic
from typing import Optional


class Post(pydantic.BaseModel):
    title: str
    content: str
    published: Optional[bool]
