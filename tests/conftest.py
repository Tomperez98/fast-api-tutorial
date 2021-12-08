from src import database, main
from fastapi.testclient import TestClient
import pytest
from tests import database_conf

FIXTURE_SCOPE = "module"


@pytest.fixture(scope=FIXTURE_SCOPE)
def session():
    database.Base.metadata.drop_all(bind=database_conf.engine)
    database.Base.metadata.create_all(bind=database_conf.engine)
    db = database_conf.TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope=FIXTURE_SCOPE)
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    main.app.dependency_overrides[database.get_db] = override_get_db
    yield TestClient(main.app)
