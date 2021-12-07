from tests.config_test_database import client, session


def test_root(client):
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}
