from fastapi import Response, status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils,database,oauth2
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote:schemas.vote,  db: Session = Depends(database.get_db),current_user:int = Depends(oauth2.get_current_user)):
    # dir =0 to delte a vote
    # dir =1 to create a vote
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote=vote_query.first()
  
    post = db.query(models.post).filter(models.post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Sorry, post with id {vote.post_id } not found") 
    if(vote.dir):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail="You have already voted for this post")
        
        new_vote = models.Vote(post_id=vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"new_vote":"success"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="You have not voted for this post")
        
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"deleted_vote":"success"}
