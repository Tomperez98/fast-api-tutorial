from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List
from src import database, models
from src.utils import oauth2
from src.schemas.request import request_post, request_token
from src.schemas.response import response_post

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get(
    "/",
    status_code=status.HTTP_302_FOUND,
    response_model=List[response_post.ExistingPost],
)
def get_all_posts(
    db: Session = Depends(database.get_db),
    current_user: request_token.TokenData = Depends(oauth2.get_current_user),
):
    posts = db.query(models.Post).all()
    return posts


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=response_post.CreatedPost,
)
def create_posts(post: request_post.Post, db: Session = Depends(database.get_db)):
    post = post.dict()
    new_post = models.Post(**post)

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get(
    "/{id}",
    status_code=status.HTTP_302_FOUND,
    response_model=response_post.ExistingPost,
)
def get_one_post(id: int, db: Session = Depends(database.get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id}"
        )
    return post


@router.delete("/{id}", status_code=status.HTTP_200_OK)
def delete_one_post(
    id: int,
    db: Session = Depends(database.get_db),
    current_user: request_token.TokenData = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id}"
        )
    else:
        post_query.delete(synchronize_session=False)

    db.commit()
    return {"response": f"Post with id {id} has been deleted"}


@router.put(
    "/{id}",
    status_code=status.HTTP_202_ACCEPTED,
    response_model=response_post.CreatedPost,
)
def update_one_post(
    id: int,
    post: request_post.Post,
    db: Session = Depends(database.get_db),
    current_user: request_token.TokenData = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)

    if not post_query.first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id}"
        )
    else:
        post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
