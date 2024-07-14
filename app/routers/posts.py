from fastapi import status,HTTPException,Response,Depends,APIRouter
from .. import models,schemas,oauth2
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List,Optional

router=APIRouter(
    prefix="/posts",
    tags=["posts"]
)

@router.get("/",response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db),search: Optional[str]=""):
    posts=db.query(models.post).filter(models.post.title.contains(search)).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(new_post:schemas.PostCreate, db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    post_dict = models.post(owner_id=current_user.id, **new_post.dict())
    db.add(post_dict)
    db.commit()
    db.refresh(post_dict)

    return post_dict

@router.get("/latest", response_model=schemas.PostResponse)
def get_latest_post(db: Session = Depends(get_db)):
    post_dict=db.query(models.post).order_by(models.post.created_at.desc()).first()
    return post_dict

@router.get("/{id}" , response_model=schemas.PostResponse)
def get_post(id:int, db: Session = Depends(get_db)):
    post_dict = db.query(models.post).filter(models.post.id==id).first()
    if post_dict:
        return post_dict

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"sorry, post with id {id} not found")


@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db) ,current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.post).filter(models.post.id==id)
    post_dict = post_query.first()

    if  post_dict==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"Sorry, post with id {id} not found")
    
    if post_dict.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requests action")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}" ,status_code= status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(id:int, updated_post:schemas.PostCreate,db: Session = Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.post).filter(models.post.id==id)
    post_dict = post_query.first()

    if post_dict == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Sorry, post with id {id} not found")
    
    if post_dict.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requests action")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()
