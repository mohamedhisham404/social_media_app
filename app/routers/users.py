from fastapi import status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..database import get_db

router=APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,  db: Session = Depends(get_db)):
    #creat hashed password
    hashed_password = utils.hash(user.password)
    user.password =  hashed_password

    #create user
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/users/{id}" , response_model=schemas.UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):
    user_dict = db.query(models.User).filter(models.User.id==id).first()
    if user_dict:
        return user_dict

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"sorry, user with id {id} not found")