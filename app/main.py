from fastapi import FastAPI,status,HTTPException,Response,Depends
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from . import models
from.database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class post(BaseModel):
    title: str
    content: str
    published: bool = True
    created_at: Optional[str] = None

while True:
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="fastAPI ",
            user="postgres",
            password="mohamed2468",
            cursor_factory=RealDictCursor # to get dict instead of tuple(column names)
        )
        cur = conn.cursor()
        print("connected")
        break
    except (Exception, psycopg2.Error) as error :
        print ("Error while connecting to PostgreSQL", error)
        time.sleep(1)

@app.get("/")
def read_root():
    return {"hello": "World"}   

@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.post).all()
    return {"data":posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(new_post:post, db: Session = Depends(get_db)):
    post_dict = models.post(**new_post.dict())
    db.add(post_dict)
    db.commit()
    db.refresh(post_dict)

    return {"data":post_dict}

@app.get("/posts/latest")
def get_latest_post(db: Session = Depends(get_db)):
    post_dict=db.query(models.post).order_by(models.post.created_at.desc()).first()
    return {"data":post_dict}

@app.get("/posts/{id}")
def get_post(id:int, db: Session = Depends(get_db)):
    post_dict = db.query(models.post).filter(models.post.id==id).first()
    if post_dict:
        return {"data":post_dict}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"sorry, post with id {id} not found")


@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int, db: Session = Depends(get_db)):
    post_query = db.query(models.post).filter(models.post.id==id)
    post_dict = post_query.first()

    if  post_dict==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"Sorry, post with id {id} not found")
    
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}" ,status_code= status.HTTP_202_ACCEPTED)
def update_post(id:int, updated_post:post,db: Session = Depends(get_db)):
    post_query = db.query(models.post).filter(models.post.id==id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Sorry, post with id {id} not found")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return {"data",post_query.first()}