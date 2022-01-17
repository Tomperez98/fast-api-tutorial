from sqlalchemy.sql import schema, sqltypes
from app.database import Base


class Vote(Base):
    __tablename__ = "votes"

    user_id = schema.Column(
        sqltypes.INTEGER,
        schema.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
    post_id = schema.Column(
        sqltypes.INTEGER,
        schema.ForeignKey("posts.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
        primary_key=True,
    )
