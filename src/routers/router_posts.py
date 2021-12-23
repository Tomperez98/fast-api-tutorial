from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from src import database, models
from src.utils import oauth2
from src.schemas.request import request_post
from src.schemas.response import response_post, response_user

router = APIRouter(prefix="/posts", tags=["posts"])


@router.get(
    "/",
    status_code=status.HTTP_302_FOUND,
    response_model=List[response_post.ExistingPost],
)
def get_all_posts(
    db: Session = Depends(database.get_db),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    posts = (
        db.query(models.Post)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return posts


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=response_post.CreatedPost,
)
def create_posts(
    post: request_post.Post,
    db: Session = Depends(database.get_db),
    current_user: response_user.ExistingUser = Depends(oauth2.get_current_user),
):
    post_dict = post.dict()
    new_post = models.Post(**post_dict, owner_id=current_user.id)

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
    current_user: response_user.ExistingUser = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id}"
        )
    elif post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
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
    current_user: response_user.ExistingUser = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    if not existing_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"No post with id {id}"
        )
    elif existing_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized"
        )
    else:
        post_query.update(post.dict(), synchronize_session=False)

    db.commit()

    return post_query.first()
