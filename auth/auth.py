from fastapi import APIRouter, BackgroundTasks, Depends,HTTPException,status
from pydantic import EmailStr
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.hashing import Hash
from db import models
from sqlalchemy import or_
from fastapi.security import OAuth2PasswordRequestForm
from auth.Oauth2 import create_access_token
from db import db_email


router = APIRouter(
    tags=["Authentication"]
   )


@router.post("/login")
def login(background_task : BackgroundTasks,credintial: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    
    query = db.query(models.DbUser).filter(or_(models.DbUser.email == credintial.username,models.DbUser.username == credintial.username )).first()
    if not query:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="user not found")
    if query.is_verified ==False:
        raise HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail="user is not verified")
    
    if not Hash.verify(credintial.password, query.password):
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="Invalid credintial")
    
    access_token = create_access_token({"username": query.username})
    if "@" in credintial.username:
        
        db_email.send_email_background(background_task,{"title": f"Dear {credintial.username},", "inf":"Someone signed-in to your account.","link":"https://www.youtube.com"},"Action neeeded: Sign-in",query.email,"login_email.html") 
    else:    
        db_email.send_email_background(background_task,{"title": f"Dear {credintial.username},", "inf":"Someone signed-in to your account.", "link":"https://www.youtube.com"},"Action neeeded: Sign-in",query.email ,"login_email.html") 

    return{
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": query.id,
        "user_name": query.username
        
        
    }
    