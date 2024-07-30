from fastapi import status,HTTPException
from .utils import hash
from sqlalchemy.orm import Session
from schemas import users as usesrsSchema
from models import users as userModel

def create_user(user:usesrsSchema.UserCreate,  db: Session):
    #creat hashed password
    hashed_password = hash(user.password)
    user.password =  hashed_password

    #create user
    new_user = userModel.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

def get_user(id:int, db: Session):
    user_dict = db.query(userModel.User).filter(userModel.User.id==id).first()
    if user_dict:
        return user_dict

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"sorry, user with id {id} not found")