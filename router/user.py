import random
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException,UploadFile,File,status
from pydantic import EmailStr
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.db_users import create_user
from router import schemas
from typing import List, Optional
from db import models,db_email
from db.hashing import Hash
from auth import Oauth2

from router.schemas import UserBase, UserDisplay

router = APIRouter(
    prefix="/users",
    tags=["Users"]
    
)

@router.post("",response_model=UserDisplay)
async def create_users(background_tasks:BackgroundTasks,request: UserBase = Depends(),image:Optional[UploadFile]= File(None),db: Session = Depends(get_db)):
   
    response =  create_user(request= request,db=db,image= image)

    otp = random.randrange(100000,999999)
    
    email_verification=models.DbOTP(
        
        username= request.username,
        otp = Hash.bcrypt(str(otp))
        
        
    )
    db.add(email_verification)
    db.commit()
    db_email.send_email_background(background_tasks,{'title': " Your onr time Password(OTP) is: ", 'otp':otp}, "Email Verification",   
    request.email,"email.html")
    
    return response 

#email verification

@router.get("/email_verify")
def email_verification(username: str,otp:int,db:Session= Depends(get_db)):
    
    is_present= db.query(models.DbOTP).filter(models.DbOTP.username==username).first()
    if not is_present:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plz click on resend otp")
    
    if not Hash.verify(str(otp),is_present.otp):
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=False)
    if Hash.verify(str(otp),is_present.otp):
        is_user_present= db.query(models.DbUser).filter(models.DbUser.username==username)
        if not is_user_present.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have to signup again")
        
        is_user_present.update({"is_verified" : True})
        db.commit()
        db.delete(is_present)
        db.commit()
        return {"detail":True}
    





#Resend otp for email verification
@router.post("/resend_otp")
async def resend(background_task:BackgroundTasks,username:str,email:EmailStr,db: Session = Depends(get_db)):
    otp = random.randrange(100000,999999)
    is_user_register=  db.query(models.DbUser).filter(models.DbUser.username==username).first()  
    if not  is_user_register:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="You have to signup") 
    
    if is_user_register and is_user_register.is_verified ==True:
        raise HTTPException(status_code=status.HTTP_410_GONE, detail="You do not need to send otp, go and just sign in") 
    if is_user_register and is_user_register.is_verified == False:

        is_present =  db.query(models.DbOTP).filter(models.DbOTP.username==username).first()
        if is_present:
            db.delete(is_present)
            db.commit()
            email_verification=models.DbOTP(
            
            username= username,
            otp = Hash.bcrypt(str(otp))
            
            
            )
            db.add(email_verification)
            db.commit()
            db_email.send_email_background(background_task,{'title': " Your one time Password(OTP) is:  ", 'otp':otp}, "Email Verification",   
            email,"email.html") 
            return {"detail":True}
        
        
        
            
        email_verification=models.DbOTP(
                
            username= username,
            otp = Hash.bcrypt(str(otp))
                
                
            )
        db.add(email_verification)
        db.commit()
        db_email.send_email_background(background_task,{'title': " Your one time Password(OTP) is:  ", 'otp':otp}, "Email Verification",   
            email,"email.html") 
        return {"detail":True}   
        
    

  
@router.get("/all",response_model=List[schemas.UserDisplay] )  
def get_all_user(db: Session = Depends(get_db), current_user: schemas.LoginBase =Depends(Oauth2.get_current_user) ):
    users =  db.query(models.DbUser).all()
    return users  



@router.get("/username_check")
async def username_check(username:str,db:Session= Depends(get_db)):
    query = db.query(models.DbUser).filter(models.DbUser.username==username).first()
    if query and query.is_verified==True:
        return {"isValid": False}
    return {"isValid": True}
    
           