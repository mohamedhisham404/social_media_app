from fastapi import FastAPI,Response,status,HTTPException
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating:Optional[int] = None

my_posts=[{"title":"title of post", "content":"content of post" , "id":1},
          {"title":"title of post 2", "content":"content of post 2" , "id":2}]

@app.get("/")
def read_root():
    return {"hello": "World"}

@app.get("/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(new_post:post):
    post_dict=new_post.dict()
    post_dict["id"] = (0, 1000000)

    my_posts.append(post_dict)
    return {"data":post_dict}

@app.get("/posts/latest")
def get_latest_post():
    return my_posts[-1]

@app.get("/posts/{id}")
def get_post(id:int ,response:Response):
    for post in my_posts:
        if post["id"] == id:
            return {"post_detail":post}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                        detail=f"sorry, post with id {id} not found")

