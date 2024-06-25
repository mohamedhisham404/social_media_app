import time
import psycopg2
from fastapi import FastAPI
from psycopg2.extras import RealDictCursor
from . import models
from.database import engine
from .routers import users,posts

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

app.include_router(users.router)
app.include_router(posts.router)

@app.get("/")
def read_root():
    return {"hello": "World"}   


