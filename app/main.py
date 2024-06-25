import time
import psycopg2
from fastapi import FastAPI,status,HTTPException,Response,Depends
from psycopg2.extras import RealDictCursor
from typing import List
from sqlalchemy.orm import Session
from . import models,schemas,utils
from.database import engine,get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#######################################database#######################################
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

#######################################posts#######################################

@app.get("/")
def read_root():
    return {"hello": "World"}   

@app.get("/posts",response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts=db.query(models.post).all()
    return posts

@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(new_post:schemas.PostCreate, db: Session = Depends(get_db)):
    post_dict = models.post(**new_post.dict())
    db.add(post_dict)
    db.commit()
    db.refresh(post_dict)

    return post_dict

@app.get("/posts/latest", response_model=schemas.PostResponse)
def get_latest_post(db: Session = Depends(get_db)):
    post_dict=db.query(models.post).order_by(models.post.created_at.desc()).first()
    return post_dict

@app.get("/posts/{id}" , response_model=schemas.PostResponse)
def get_post(id:int, db: Session = Depends(get_db)):
    post_dict = db.query(models.post).filter(models.post.id==id).first()
    if post_dict:
        return post_dict

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

@app.put("/posts/{id}" ,status_code= status.HTTP_202_ACCEPTED, response_model=schemas.PostResponse)
def update_post(id:int, updated_post:schemas.PostCreate,db: Session = Depends(get_db)):
    post_query = db.query(models.post).filter(models.post.id==id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Sorry, post with id {id} not found")

    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()

#######################################users#######################################

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserResponse)
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

@app.get("/users/{id}" , response_model=schemas.UserResponse)
def get_user(id:int, db: Session = Depends(get_db)):
    user_dict = db.query(models.User).filter(models.User.id==id).first()
    if user_dict:
        return user_dict

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"sorry, user with id {id} not found")