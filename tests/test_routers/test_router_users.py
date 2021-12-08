from src.schemas.response import response_user, response_token
from src.utils import oauth2
from jose import jwt


def test_create_user(client):
    response = client.post(
        url="/users/", json={"email": "nuevaao@gmail.com", "password": "123"}
    )

    new_user = response_user.CreatedUser(**response.json())
    assert response.status_code == 201
    assert new_user.email == "nuevaao@gmail.com"
    assert new_user.id == 1


def test_login_user(client):
    client.post(url="/users/", json={"email": "nuevaao@gmail.com", "password": "123"})

    response = client.post(
        url="/auth/login", data={"username": "nuevaao@gmail.com", "password": "123"}
    )

    login_res = response_token.PlainToken(**response.json())
    payload = jwt.decode(
        token=login_res.access_token,
        key=oauth2.SECRET_KEY,
        algorithms=[oauth2.ALGORITHM],
    )
    user_id = payload.get("user_id")
    assert response.status_code == 202
    assert user_id == 1
