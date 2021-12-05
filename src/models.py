from sqlalchemy.sql import schema, sqltypes, expression
from src.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = schema.Column(sqltypes.INTEGER, primary_key=True, nullable=False)
    title = schema.Column(sqltypes.VARCHAR, nullable=False)
    content = schema.Column(sqltypes.VARCHAR, nullable=False)
    published = schema.Column(sqltypes.BOOLEAN, server_default="TRUE", nullable=False)
    created_at = schema.Column(
        sqltypes.TIMESTAMP(timezone=True),
        nullable=False,
        server_default=expression.text("CURRENT_TIMESTAMP"),
    )


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
