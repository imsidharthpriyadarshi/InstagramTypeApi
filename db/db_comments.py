from fastapi import HTTPException, status
from sqlalchemy.orm.session import Session
from  db import models
from router import schemas
from router.schemas import CommentBase


def create_comments(db: Session, request: CommentBase,current_user :schemas.LoginBase):
    is_post= db.query(models.DbPost).filter(models.DbPost.id==request.post_id).first()
    if not is_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="post not found")
    is_user= db.query(models.DbUser).filter(models.DbUser.username==current_user.username).first()
    if not is_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    new_comments= models.DbComment(
        
        
        text = request.text,
        username= current_user.username,
        post_id= request.post_id
        
        
    )
    db.add(new_comments)
    db.commit()
    db.refresh(new_comments)
    return new_comments


def get_all(db: Session, post_id: int):
    return db.query(models.DbComment).filter(models.DbComment.post_id==post_id).all()