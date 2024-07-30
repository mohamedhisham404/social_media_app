from fastapi import status,Depends,APIRouter
from .. import oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional
from ..crud import posts
from schemas import posts as postsSchema

router=APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/",response_model=List[postsSchema.PostResponse])
def get_posts(db: Session = Depends(get_db),search: Optional[str]=""):
    return posts.get_posts(db, search)
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=postsSchema.PostResponse)
def create_posts(new_post:postsSchema.PostCreate, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    return posts.create_posts(new_post,db,current_user)

@router.get("/latest", response_model=postsSchema.PostResponse)
def get_latest_post(db: Session = Depends(get_db)):
    return posts.get_latest_post(db)

@router.get("/{id}" , response_model=postsSchema.PostResponse)
def get_post(id:int, db: Session = Depends(get_db)):
    return posts.get_post(id,db)


@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db) ,current_user:int = Depends(oauth2.get_current_user)):
    return posts.delete_post(id,db,current_user)

@router.put("/{id}" ,status_code= status.HTTP_202_ACCEPTED, response_model=postsSchema.PostResponse)
def update_post(id:int, updated_post:postsSchema.PostCreate,db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    return posts.update_post(db, id, updated_post, current_user.id)

