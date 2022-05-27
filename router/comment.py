from fastapi import APIRouter, Depends
from auth.Oauth2 import get_current_user
from db.database import get_db
from db import db_comments
from sqlalchemy.orm.session import Session
from router import schemas


router = APIRouter(
    
    prefix="/comments",
    tags=["Comments"]
)


@router.get('/all/{post_id}')
def commments(post_id:int, db: Session= Depends(get_db), current_user: schemas.LoginBase =Depends(get_current_user) ):
    return db_comments.get_all(db,post_id)



@router.post("")
def create(request: schemas.CommentBase,db: Session= Depends(get_db), current_user: schemas.LoginBase =Depends(get_current_user)):
    return db_comments.create_comments(db,request,current_user=current_user)