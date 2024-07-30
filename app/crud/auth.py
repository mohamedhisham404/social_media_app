from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app.crud import utils
from app import  oauth2
from models import users as usersModel

def authenticate_user(db: Session, username: str, password: str):
    user_dict = db.query(usersModel.User).filter(usersModel.User.email == username).first()
    if not user_dict:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"sorry, user with email {username} not found")

    if not utils.verify(password, user_dict.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"sorry, password is incorrect")

    access_token = oauth2.create_access_token(data={"user_id": user_dict.id})
    return {"access_token": access_token, "token_type": "bearer"}
