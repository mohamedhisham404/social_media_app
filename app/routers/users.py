from fastapi import status,HTTPException,Depends,APIRouter
from .. import models,schemas,utils
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import users

router=APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,  db: Session = Depends(get_db)):
    return users.create_user(user,db)

@router.get("/{id}" , response_model=schemas.UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):
    return users.get_user(id,db)