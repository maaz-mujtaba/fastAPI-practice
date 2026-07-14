from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from passlib.context import CryptContext
from .. import models, schemas, utility
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(
    prefix="/users",
    tags = ["Users"]
)


@router.post('/login', response_model = schemas.Token)
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Invalid Credentials"
        )
    return user

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user : schemas.UserCreate, db : Session = Depends(get_db), ):

    #hash the password

    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}", response_model=schemas.UserOut)
def get_user(id : int, db : Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id)

    if not user.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
    return user.first()