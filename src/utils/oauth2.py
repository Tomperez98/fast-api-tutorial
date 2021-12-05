from jose import JWTError, jwt
from pydantic import validate_arguments
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from src.schemas.request import request_token
from src import database, models
from sqlalchemy.orm import Session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# TODO: This 3 constants (SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES)
# should be in a config file
SECRET_KEY = "e0aa47ea42bf686936118aeaab910d44789d2a1d40e61cb003d0ec557a2e6be2"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


@validate_arguments
def create_access_token(data: dict):
    to_encode = data.copy()

    expire_at = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire_at})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


@validate_arguments
def _verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])

        # TODO: If data required to create_access_token changes, each
        # individual attribute has to be extracted here
        user_id = payload.get("user_id")

        if user_id is None:
            raise credentials_exception

        token_data = request_token.TokenData(user_id=user_id)

    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_verified = _verify_access_token(token, credentials_exception)

    current_user = (
        db.query(models.User).filter(models.User.id == token_verified.user_id).first()
    )

    return current_user
