import pydantic
from enum import Enum


class Direction(int, Enum):
    ZERO = 0
    ONE = 1


class CreateVote(pydantic.BaseModel):
    post_id: int
    dir: Direction
