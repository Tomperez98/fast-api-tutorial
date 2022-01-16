import jose
from jose import jwt
import pydantic
import datetime
from fastapi import status
import fastapi
from fastapi import security
from app.schemas.request import request_token
from app import database, models
from app.config import settings
from sqlalchemy import orm

oauth2_scheme: security.OAuth2PasswordBearer = security.OAuth2PasswordBearer(
    tokenUrl="/auth/login"
)

# TODO: This 3 constants (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)
# should be in a config file
SECRET_KEY: str = settings.defined_settings.SECRET_KEY
ALGORITHM: str = settings.defined_settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES: int = settings.defined_settings.ACCESS_TOKEN_EXPIRE_MINUTES


@pydantic.validate_arguments
def create_access_token(data: dict):
    to_encode = data.copy()

    expire_at = datetime.datetime.utcnow() + datetime.timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    to_encode.update({"exp": expire_at})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


@pydantic.validate_arguments
def _verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])

        # TODO: If data required to create_access_token changes, each
        # individual attribute has to be extracted here
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data = request_token.TokenData(user_id=user_id)

    except jose.JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = fastapi.Depends(oauth2_scheme),
    db: orm.Session = fastapi.Depends(database.get_db),
):
    credentials_exception = fastapi.HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_verified = _verify_access_token(token, credentials_exception)

    current_user = (
        db.query(models.User).filter(models.User.id == token_verified.user_id).first()
    )

    return current_user
