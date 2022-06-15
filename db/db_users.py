import random
import shutil
import string
from typing import Optional
from fastapi import BackgroundTasks, Depends, File, HTTPException, UploadFile,status
from sqlalchemy.orm.session import Session
from sqlalchemy import null, or_
from db.models import DbUser
from router.schemas import UserBase
from db.hashing import Hash
from db import models,db_email

def create_user(request : UserBase,db: Session,image:UploadFile= File(...)):
    existing_user = db.query(models.DbUser).filter(models.DbUser.email== request.email).first()
    if existing_user and existing_user.is_verified==True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with this email already exist")
    
    existing_username = db.query(models.DbUser).filter(models.DbUser.username== request.username).first()
    if existing_username and existing_username.is_verified==True:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with this username already exist")
    
    if image :
    
        if (existing_user and existing_user.is_verified==False ) :
            db.delete(existing_user)
            db.commit()
            letters=string.ascii_letters
            rand_str = ''.join(random.choice(letters) for i in range(10))
            new = f'_{rand_str}.'
            filename = new.join(image.filename.rsplit('.',1))
            path = f'images/user/{filename}'
            
            with open(path, "w+b") as buffer:
                shutil.copyfileobj(image.file,buffer)

            
            new_user = DbUser(
                profile_pic = path,
                username= request.username,
                email = request.email,
                password= Hash.bcrypt(request.password)
            
                )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
            
        
        if (existing_username and existing_username.is_verified==False ):
            db.delete(existing_username)
            db.commit()
            letters=string.ascii_letters
            rand_str = ''.join(random.choice(letters) for i in range(10))
            new = f'_{rand_str}.'
            filename = new.join(image.filename.rsplit('.',1))
            path = f'images/user/{filename}'
            
            with open(path, "w+b") as buffer:
                shutil.copyfileobj(image.file,buffer)

            
            new_user = DbUser(
                profile_pic = path,
                username= request.username,
                email = request.email,
                password= Hash.bcrypt(request.password)
            
                )
            db.add(new_user)
            db.commit()
            db.refresh(new_user)
            return new_user
            
        letters=string.ascii_letters
        rand_str = ''.join(random.choice(letters) for i in range(10))
        new = f'_{rand_str}.'
        filename = new.join(image.filename.rsplit('.',1))
        path = f'images/user/{filename}'
        
        with open(path, "w+b") as buffer:
            shutil.copyfileobj(image.file,buffer)

        
        new_user = DbUser(
            profile_pic = path,
            username= request.username,
            email = request.email,
            password= Hash.bcrypt(request.password)
        
            )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    
    new_user = DbUser(
            profile_pic = "images/user/default.jpg",
            username= request.username,
            email = request.email,
            password= Hash.bcrypt(request.password)
        
            )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
    
    




def get_user_by_username(db:Session,username : str):
    user =db.query(models.DbUser).filter(models.DbUser.username== username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="username not found")
    
    return user