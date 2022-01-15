from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings


TEST_DATABASE_URL = "postgresql://{username}:{password}@{host}:{port}/{database}".format(
    username=settings.defined_settings.POSTGRES_USER,
    password=settings.defined_settings.POSTGRES_PASSWORD,
    host=settings.defined_settings.HOST_TEST_DB,
    port=settings.defined_settings.EXPOSED_PORT,
    database=settings.defined_settings.POSTGRES_DB,
)

engine = create_engine(TEST_DATABASE_URL)

# TEST_DATABASE_URL = "sqlite:///./test_sql_app.db"

# engine = create_engine(
#     TEST_DATABASE_URL, connect_args={"check_same_thread": False}
# )

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
