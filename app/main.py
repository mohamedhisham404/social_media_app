from fastapi import FastAPI
from . import models
from.database import engine
from .routers import users,posts,auth
from .config import Settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# while True:
#     try:
#         conn = psycopg2.connect(
#             host="",
#             database=" ",
#             user="postgres",
#             password="",
#             cursor_factory=RealDictCursor # to get dict instead of tuple(column names)
#         )
#         cur = conn.cursor()
#         print("connected")
#         break
#     except (Exception, psycopg2.Error) as error :
#         print ("Error while connecting to PostgreSQL", error)
#         time.sleep(1)

app.include_router(users.router)
app.include_router(posts.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"hello": "World"}   


