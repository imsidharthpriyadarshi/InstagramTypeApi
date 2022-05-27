
from operator import and_
from fastapi import APIRouter, Depends,HTTPException,status
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.hashing import Hash
from db import models
from sqlalchemy import and_,or_
from fastapi.security import OAuth2PasswordRequestForm
from auth.Oauth2 import create_access_token


router = APIRouter(
    tags=["Authentication"]
   )


@router.post("/login")
def login(credintial: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    query = db.query(models.DbUser).filter(or_(models.DbUser.email == credintial.username,models.DbUser.username == credintial.username )).first()
    if not query:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="user not found")
    
    if not Hash.verify(credintial.password, query.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Invalid credintial")
    
    access_token = create_access_token({"username": query.username})
    
    return{
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": query.id,
        "user_name": query.username
        
        
    }
    