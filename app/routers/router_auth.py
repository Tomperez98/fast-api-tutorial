import fastapi
from fastapi import status
from fastapi.security import oauth2
from sqlalchemy import orm
from app.schemas.response import response_token
from app import database, models
from app.utils import security, auth

router = fastapi.APIRouter(prefix="/auth", tags=["authentication"])


@router.post(
    "/login", status_code=status.HTTP_202_ACCEPTED, response_model=response_token.PlainToken
)
def login(
    user_credentials: oauth2.OAuth2PasswordRequestForm = fastapi.Depends(),
    db: orm.Session = fastapi.Depends(database.get_db),
):
    user = (
        db.query(models.User)
        .filter(models.User.email == user_credentials.username)
        .first()
    )

    if not user:
        raise fastapi.HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )

    password_match = security.verify_password(
        plain_password=user_credentials.password, hashed_password=user.password
    )

    if not password_match:
        raise fastapi.HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid credentials",
        )

    # TODO: At the moment only user_id is used to do the encoding. To be defined
    # which other attributes will be used
    access_token = auth.create_access_token(data={"user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
