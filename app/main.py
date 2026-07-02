from dbm import error
from typing import Optional
from django import db
from django import db
from fastapi import Body, FastAPI, Response,status,HTTPException, Depends
from fastapi.params import Body
from matplotlib.pyplot import title
import psycopg2
from pydantic import BaseModel
from random import randrange
from psycopg2.extras import RealDictCursor
import time
from sqlalchemy.orm import Session
from app import models
from database import engine,  get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#schemas


class Post(BaseModel):
    title : str
    content : str
    published : bool = True
     
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='maaz1234', cursor_factory=psycopg2.extras.RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)





@app.get("/")
async def read_root():
    return {"message": "World"}

@app.get("/sqlalchemy")
async def test_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    return {"data": posts}

@app.get("/msg")
async def msg():
    return {"message": "Hello World"}

my_posts = [{"title": "title of post 1", "content": "content of post 1","id": 1}, {"title": "favorite foods", "content": "I like pizza","id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

@app.get("/posts")
async def get_posts(db : Session = Depends(get_db)):
    test_posts = db.query(models.Post).all()
    return {"data": test_posts}



@app.post("/posts")
async def createPosts(post: Post, db : Session = Depends(get_db)):

    new_post = models.Post(title = post.title, content = post.content, published = post.published)
    #sames as models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"latest_post" : post}

@app.get("/posts/{id}")
async def get_post(id : int, db : Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    return {"post_detail" : post}


 

#title, str, content str, category

def find_index_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

@app.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db : Session = Depends(get_db)):
    #deleting post
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    db.delete(post.first())
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id : int, post: Post, db : Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    updated_post.update(post.dict())
    db.commit()
    return {"data": updated_post.first()}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    db.delete(post.first())
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    