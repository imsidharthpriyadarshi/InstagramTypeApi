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
def create_users(request: UserBase = Depends(),image:UploadFile= File(...),db: Session = Depends(get_db)):
    return create_user(request= request,db=db,image= image)
    
@router.get("/all",response_model=List[schemas.UserDisplay] )  
def get_all_user(db: Session = Depends(get_db), current_user: schemas.LoginBase =Depends(Oauth2.get_current_user) ):
    users = db.query(models.DbUser).all()
    return users  

       