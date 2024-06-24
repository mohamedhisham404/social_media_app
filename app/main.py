from fastapi import FastAPI,status,HTTPException,Response
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time

app = FastAPI()

class post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[int] = None

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
def get_posts():
    cur.execute("""SELECT * FROM posts""")
    posts = cur.fetchall()
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(new_post:post):
    cur.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
                (new_post.title,new_post.content,new_post.published))
    
    post_dict=cur.fetchone()
    conn.commit()
    return {"data":post_dict}

@app.get("/posts/latest")
def get_latest_post():
    cur.execute("""SELECT * from posts ORDER BY created_at DESC LIMIT 1""")

    post_dict=cur.fetchone()
    conn.commit()
    return {"data":post_dict}

@app.get("/posts/{id}")
def get_post(id:int):
    cur.execute("""SELECT * from posts where id=%s""",(str(id)))

    post_dict=cur.fetchone()
    conn.commit()
    if post_dict:
        return {"data":post_dict}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"sorry, post with id {id} not found")


@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    cur.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    post_dict = cur.fetchone()
    conn.commit()
    
    if not post_dict:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Sorry, post with id {id} not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}" ,status_code= status.HTTP_202_ACCEPTED)
def update_post(id:int,new_post:post):
   cur.execute("""UPDATE POSTS SET title=%s,content=%s,published=%s WHERE id=%s RETURNING *""",
               (new_post.title,new_post.content,new_post.published,str(id)))
   
   post_dict = cur.fetchone()
   conn.commit()

   if not post_dict:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                           detail=f"Sorry, post with id {id} not found")
   
   return {"data":post_dict}