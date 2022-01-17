from sqlalchemy.sql import schema, sqltypes, expression
from app.database import Base


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
