from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from src import database, models
from src.schemas.request import request_user
from src.schemas.response import response_user
from src.utils import security

router = APIRouter(prefix="/users", tags=["users"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=response_user.CreatedUser,
)
def create_user(user: request_user.User, db: Session = Depends(database.get_db)):

    user.password = security.password_hasher(plain_password=user.password)
    user = user.dict()
    new_user = models.User(**user)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@router.get(
    "/{id}",
    status_code=status.HTTP_302_FOUND,
    response_model=response_user.ExistingUser,
)
def get_one_user(id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No user found with id {id}"
        )

    return user
