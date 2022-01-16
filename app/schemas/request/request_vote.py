import pydantic
import enum


class Direction(int, enum.Enum):
    ZERO = 0
    ONE = 1


class CreateVote(pydantic.BaseModel):
    post_id: int
    dir: Direction
