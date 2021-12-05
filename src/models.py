from sqlalchemy.orm import relationship
from sqlalchemy.sql import schema, sqltypes, expression
from src.database import Base


# TODO: Test CASCADE definitions. Seems not to work with SQLite
class Post(Base):
    __tablename__ = "posts"

    id = schema.Column(sqltypes.INTEGER, primary_key=True, nullable=False)
    title = schema.Column(sqltypes.VARCHAR, nullable=False)
    content = schema.Column(sqltypes.VARCHAR, nullable=False)
    published = schema.Column(sqltypes.BOOLEAN, server_default="TRUE", nullable=False)
    created_at = schema.Column(
        sqltypes.TIMESTAMP(timezone=True),
        nullable=False,
        # TODO: When using postgresql replace CURRENT_TIMESTAMP with NOW()
        server_default=expression.text("CURRENT_TIMESTAMP"),
    )

    owner_id = schema.Column(
        sqltypes.INTEGER,
        schema.ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    owner = relationship("User")


class User(Base):
    __tablename__ = "users"

    id = schema.Column(sqltypes.INTEGER, primary_key=True, nullable=False)
    email = schema.Column(sqltypes.VARCHAR, nullable=False, unique=True)
    password = schema.Column(sqltypes.VARCHAR, nullable=False)
    created_at = schema.Column(
        sqltypes.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=expression.text("CURRENT_TIMESTAMP"),
    )