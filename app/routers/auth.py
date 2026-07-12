from fastapi import APIRouter, Depends, HTTPException, status, HTTPExcepyion, Response
from sqlalchemy import Session
from app import database, models,schemas, utility


router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials : schemas.UserLogin, db : Session = Depends(database.get_db)):

    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utility.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    #create a token
    return {"message" : "Successfully logged in!"}
    