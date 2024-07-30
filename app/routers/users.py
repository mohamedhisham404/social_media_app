from fastapi import status,Depends,APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from ..crud import users
from schemas import users as usersSchema
router=APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=usersSchema.UserResponse)
def create_user(user:usersSchema.UserCreate,  db: Session = Depends(get_db)):
    return users.create_user(user,db)

@router.get("/{id}" , response_model=usersSchema.UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):
    return users.get_user(id,db)