from tests import config_test_database
from src.schemas.response import response_user

test_client = config_test_database.client


def test_root(test_client):
    response = test_client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_create_user(test_client):
    response = test_client.post(
        url="/users/", json={"email": "nuevaao@gmail.com", "password": "123"}
    )

    new_user = response_user.CreatedUser(**response.json())
    assert response.status_code == 201
    assert new_user.email == "nuevaao@gmail.com"
    assert new_user.id == 1
