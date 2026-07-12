from typing import Optional
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
import schemas
from utility import pwd_context
from app.routers import post, user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#schemas



     
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='maaz1234', cursor_factory=psycopg2.extras.RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)



def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p

app.include_router(post.router)
app.include_router(user.router)


