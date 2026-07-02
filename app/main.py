from dbm import error
from typing import Optional
from fastapi import Body, FastAPI, Response,status,HTTPException
from fastapi.params import Body
import psycopg2
from pydantic import BaseModel
from random import randrange
from psycopg2.extras import RealDictCursor


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

@app.get("/msg")
async def msg():
    return {"message": "Hello World"}

my_posts = [{"title": "title of post 1", "content": "content of post 1","id": 1}, {"title": "favorite foods", "content": "I like pizza","id": 2}]

def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

@app.get("/posts")
async def get_posts():
    cursor.execute("""SELECT * FROM posts where id = %s""", (str(id)))
    test_post = cursor.fetchone()
    print(test_post)
    posts = cursor.fetchall()
    return {"data": test_post}



@app.post("/posts")
async def createPosts(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    print(post.title)
    print(post.dict())
    post_dict = post.dict()
    post_dict['id'] = randrange(0,100000)
    my_posts.append(post_dict)
    return {"data": post}

@app.get("/posts/latest")
async def get_latest_post():
    post = my_posts[len(my_posts) - 1]
    return {"latest_post" : post}

@app.get("/posts/{id}")
async def get_post(id : int, response: Response):
    print(id)
    post = find_post(id)

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
def delete_post(id : int,):
    #deleting post
    # find the index in the array
    index = find_index_post(id)
    if index is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
async def update_post(id : int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone() 
    conn.commit()       
    
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")

    
    return {"data" : updated_post}

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
     
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with id: {id} does not exist")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)