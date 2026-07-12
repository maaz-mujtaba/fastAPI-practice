from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schemas, utility
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)

@router.get("/")
def read_root():
    return {"message": "World"}
def read_root():
    return {"message": "World"}

@router.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    return {"data": posts}

@router.get("/msg")
def msg():
    return {"message": "Hello World"}

my_posts = [{"title": "title of post 1", "content": "content of post 1","id": 1}, {"title": "favorite foods", "content": "I like pizza","id": 2}]


@router.get("/", response_model = list[schemas.Post])
def get_posts(db : Session = Depends(get_db)):
    test_posts = db.query(models.Post).all()
    return {"data": test_posts}



@router.post("/",response_class=Response, status_code=status.HTTP_201_CREATED)
def createPosts(post: schemas.PostCreate, db : Session = Depends(get_db), response_model = schemas.Post):

    #new_post = models.Post(title = post.title, content = post.content, published = post.published)
    new_post =  models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"data": new_post}

@router.get("/latest")
def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"latest_post" : post}

@router.get("/{id}")
def get_post(id : int, db : Session = Depends(get_db), response_model = schemas.Post):

    post = db.query(models.Post).filter(models.Post.id==id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
    
    return {"post_detail" : post}


 

#title, str, content str, category



@router.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id : int, db : Session = Depends(get_db)):
    #deleting post
    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    db.delete(post.first())
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/posts/{id}")
def update_post(id : int, post: schemas.PostUpdate, db : Session = Depends(get_db)):
    updated_post = db.query(models.Post).filter(models.Post.id == id)
    if not updated_post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    updated_post.update(post.dict())
    db.commit()
    return {"data": updated_post.first()}

@router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    db.delete(post.first())
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)