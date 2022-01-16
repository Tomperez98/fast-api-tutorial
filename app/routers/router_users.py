import fastapi
from fastapi import status
from sqlalchemy import orm
from app import database, models
from app.schemas.request import request_user
from app.schemas.response import response_user
from app.utils import security

router = fastapi.APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=response_user.CreatedUser,
)
def create_user(
    user: request_user.User, db: orm.Session = fastapi.Depends(database.get_db)
):

    user.password = security.password_hasher(plain_password=user.password)
    user_dict = user.dict()
    new_user = models.User(**user_dict)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
    "/{id}",
    status_code=status.HTTP_302_FOUND,
    response_model=response_user.ExistingUser,
)
def get_one_user(id: int, db: orm.Session = fastapi.Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise fastapi.HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found with id {id}"
        )

    return user
