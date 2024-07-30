from fastapi import HTTPException,status,Response
from sqlalchemy.orm import Session
from typing import List,Optional
from .. import models,schemas

def get_posts(db: Session ,search: Optional[str]=""):
    posts=db.query(models.post).filter(models.post.title.contains(search)).all()
    return posts

def create_posts(new_post:schemas.PostCreate, db: Session ,current_user:int):
    post_dict = models.post(owner_id=current_user.id, **new_post.dict())
    db.add(post_dict)
    db.commit()
    db.refresh(post_dict)

    return post_dict

def get_latest_post(db: Session):
    post_dict = db.query(models.post).order_by(models.post.created_at.desc()).first()
    if not post_dict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts available")
    return post_dict

def get_post(id:int, db: Session ):
    post_dict = db.query(models.post).filter(models.post.id==id).first()
    if post_dict:
        return post_dict

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"sorry, post with id {id} not found")

def delete_post(id:int, db: Session ,current_user:int):
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

def update_post(db: Session, post_id: int, updated_post: schemas.PostCreate, user_id: int) :
    post_query = db.query(models.post).filter(models.post.id == post_id)
    post_dict = post_query.first()

    if post_dict is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Sorry, post with id {post_id} not found")
    
    if post_dict.owner_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform this action")

    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()
