from fastapi import status, Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from src import database, models
from src.utils import oauth2
from src.schemas.request import request_vote
from src.schemas.response import response_user


router = APIRouter(prefix="/votes", tags=["votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: request_vote.CreateVote,
    db: Session = Depends(database.get_db),
    current_user: response_user.ExistingUser = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    post_exists = post_query.first()
    if not post_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {vote.post_id} does not exists",
        )

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id
    )
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.id} has already vote post {vote.post_id}",
            )
        else:
            new_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)
            db.add(new_vote)
            db.commit()
            return {"message": "vote successfully added"}
    elif vote.dir == 0:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"There's no vote for post {vote.post_id} by user {current_user.id}",
            )
        else:
            vote_query.delete(synchronize_session=False)
            db.commit()
            return {"message": "vote successfully deleted"}
