from fastapi import FastAPI
from db import models
from db.database import engine
from router import user,post,comment
from fastapi.staticfiles import StaticFiles
from auth import auth

app = FastAPI()


models.Base.metadata.create_all(engine)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.include_router(comment.router)

app.mount('/images',StaticFiles(directory='images'),name='images')


@app.get("/")
def root():
    return "Yes successfully deployed"
