from typing import Optional
from fastapi import Body, FastAPI, Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange

app = FastAPI()

#schemas
class Post(BaseModel):
    title : str
    content : str
    published : bool = True
    rating : Optional[int] = None

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
    return {"data": my_posts}



@app.post("/posts")
async def createPosts(post: Post):
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