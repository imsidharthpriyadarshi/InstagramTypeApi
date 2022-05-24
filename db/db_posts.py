from router.schemas import PostBase
from sqlalchemy.orm.session import Session
from db import models
from fastapi import HTTPException,status,Response

def create(db:Session, request: PostBase):
    new_post = models.DbPost(
        
    image_url = request.image_url,
    image_url_type= request.image_url_type,
    caption= request.caption,
    user_id =request.user_id
        
    )
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post



def get_posts(db:Session):
    return db.query(models.DbPost).all()



def delete( db: Session, id:int , user_id:int ):
    print("enter")
    post_found= db.query(models.DbPost).filter(models.DbPost.id == id)
    if not post_found.first():
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="post not found")
    if  post_found.first().user_id != user_id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail="This is not your post")
    
    db.delete(post_found.first())
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    