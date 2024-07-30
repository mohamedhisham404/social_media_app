from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models
from schemas import vote as voteSchema

def create_vote(db: Session, vote: voteSchema.vote, user_id: int):
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == user_id)
    found_vote = vote_query.first()
  
    post = db.query(models.post).filter(models.post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Sorry, post with id {vote.post_id} not found")
   
    if found_vote:
        # Delete from the vote table
        vote_query.delete(synchronize_session=False)
        db.commit()
    
        # Decrease the number of votes in the post table
        post.votes -= 1
        db.commit()
        db.refresh(post)
        return {"deleted_vote": "success"}
    
    new_vote = models.Vote(post_id=vote.post_id, user_id=user_id)
    db.add(new_vote)
    db.commit()

    post.votes += 1
    db.commit()
    db.refresh(post)
    return {"new_vote": "success"}
