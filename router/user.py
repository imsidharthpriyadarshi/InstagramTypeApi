from fastapi import APIRouter, Depends,UploadFile,File
from sqlalchemy.orm.session import Session
from db.database import get_db
from db.db_users import create_user
from router import schemas
import string, random, shutil
from typing import List
from db import models
from auth import Oauth2

from router.schemas import UserBase, UserDisplay

router = APIRouter(
    prefix="/users",
    tags=["Users"]
    
)

@router.post("",response_model=UserDisplay)
def create_users(request: UserBase,db: Session = Depends(get_db)):
    return create_user(request,db)
    
@router.get("/all",response_model=List[schemas.UserDisplay] )  
def get_all_user(db: Session = Depends(get_db), current_user: schemas.LoginBase =Depends(Oauth2.get_current_user) ):
    users = db.query(models.DbUser).all()
    return users  

@router.post("/image")
def upload_image(image:UploadFile= File(...)):
    letters=string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(10))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.',1))
    path = f'images/user/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file,buffer)
        
    return {'filename': path}        