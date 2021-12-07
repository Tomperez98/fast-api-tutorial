from tests import config_test_database

test_client = config_test_database.client


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
