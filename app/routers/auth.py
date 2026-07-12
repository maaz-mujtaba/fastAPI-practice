from fastapi import APIRouter, Depends, HTTPException, status, HTTPExcepyion, Response
from sqlalchemy import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm        
from app import database, models,schemas, utility, oauth


router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials : OAuth2PasswordRequestForm = Depends(), db : Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.username ).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utility.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #create a token

    access_token = oauth.create_access_token(data = {"user_id": user.id})
    return {"message" : "Successfully logged in!", "access_token": access_token, "token_type": "bearer"}
    