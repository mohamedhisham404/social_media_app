from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from..database import get_db
from.. import models,utils,oauth2

router=APIRouter(tags=["Authentication"])


@router.post("/login")
def login(user_credentials:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user_dict = db.query(models.User).filter(models.User.email==user_credentials.username).first()
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"sorry, user with email {user_credentials.username} not found")

    if not utils.verify(user_credentials.password, user_dict.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"sorry, password is incorrect")

    access_token = oauth2.create_access_token(data={"user_id":user_dict.id})#data we want to put in payload
    return {"access_token":access_token, "token_type":"bearer"}