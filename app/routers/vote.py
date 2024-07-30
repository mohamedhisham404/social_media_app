from fastapi import status,HTTPException,Depends,APIRouter
from .. import models,schemas,database,oauth2
from sqlalchemy.orm import Session
from ..crud.vote import create_vote as vote_on_post

router=APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_vote(vote: schemas.vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    return vote_on_post(db, vote, current_user.id)

   
        
       
