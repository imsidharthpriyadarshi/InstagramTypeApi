import asyncio
from typing import List
from fastapi import APIRouter, Depends,HTTPException,status,UploadFile,File,Form
from auth.Oauth2 import get_current_user
from db.database import get_db
from db import models,db_email
from sqlalchemy.orm.session import Session


from router import schemas
from db.db_posts import create , get_posts , delete
import random
import string
import shutil
router = APIRouter(
    
    prefix="/post",
    tags=["Posts"]
)


@router.post("",response_model=schemas.PostDisplay)
def create_post(request: schemas.PostBase,db: Session= Depends(get_db),current_user: schemas.LoginBase =Depends(get_current_user)):
    response = create(request=request, db= db,current_user=current_user)
 
    return response
      
 
@router.get("/all",response_model=List[schemas.PostDisplay])
async def posts(db: Session= Depends(get_db)):
    
    posts= await get_posts(db=db)
    return posts



@router.post("/image",response_model=schemas.PostPicOut)
def upload_image(db: Session= Depends(get_db),img_post: schemas.PostId = Depends(),image:UploadFile= File(...),current_user: schemas.LoginBase =Depends(get_current_user)):
    
    is_current_user_post = db.query(models.DbPost).filter(models.DbPost.id == img_post.id)
    if not is_current_user_post.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    if is_current_user_post.first().user_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="This is not your post")


    letters=string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(8))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.',1))
    path = f'images/post/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file,buffer)
    
    
    post_photo=models.DbPostPic(image_url=path,post_id=img_post.id )
    db.add(post_photo)
    db.commit()
    db.refresh(post_photo)
    
  
    
    
        
    return post_photo    



@router.get("/delete/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.LoginBase =Depends(get_current_user)):
    return delete( db=db,id=id, user_id=current_user.id)