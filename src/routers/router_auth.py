from fastapi import Depends, APIRouter, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette.status import HTTP_202_ACCEPTED
from src.schemas.response import response_token
from src import database, models
from src.utils import security, oauth2

router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/login", status_code=HTTP_202_ACCEPTED, response_model=response_token.PlainToken
)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )

    password_match = security.verify_password(
        plain_password=user_credentials.password, hashed_password=user.password
    )

    if not password_match:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )

    # TODO: At the moment only user_id is used to do the encoding. To be defined
    # which other attributes will be used
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
