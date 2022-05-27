import random
import string
from fastapi import Depends, File, HTTPException, UploadFile,status
from sqlalchemy.orm.session import Session
from db.models import DbUser
from router.schemas import UserBase
from db.hashing import Hash
from db import models


def create_user(request : UserBase,db: Session,image:UploadFile= File(...) ):
    existing_user = db.query(models.DbUser).filter(models.DbUser.email== request.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with this email already exist")
    existing_username = db.query(models.DbUser).filter(models.DbUser.username== request.username).first()
    if existing_username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User with this username already exist")
    letters=string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(10))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.',1))
    path = f'images/user/{filename}'

    
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




def get_user_by_username(db:Session,username : str):
    user =db.query(models.DbUser).filter(models.DbUser.username== username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="username not found")
    
    return user