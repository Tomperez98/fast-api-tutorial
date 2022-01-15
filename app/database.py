from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

# DATABASE_URL = "sqlite:///./sql_app.db"
DATABASE_URL = "postgresql://{username}:{password}@{host}:{port}/{database}".format(
    username=settings.defined_settings.POSTGRES_USER,
    password=settings.defined_settings.POSTGRES_PASSWORD,
    host=settings.defined_settings.HOST_DEV_DB,
    port=settings.defined_settings.EXPOSED_PORT,
    database=settings.defined_settings.POSTGRES_DB,
)

# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
engine = create_engine(DATABASE_URL)
# connect_args={"check_same_thread": False} It's only needed for SQLite. It's not for other dbs

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
