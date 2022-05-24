from typing import List
from fastapi import APIRouter, Depends,HTTPException,status,UploadFile,File
from requests import Session
from auth.Oauth2 import get_current_user
from db.database import get_db

from router import schemas
from db.db_posts import create , get_posts , delete
import random
import string
import shutil
router = APIRouter(
    
    prefix="/post",
    tags=["Posts"]
)

image_url_types= ["absolute","relative"]

@router.post("",response_model=schemas.PostDisplay)
def create_post(request: schemas.PostBase,db: Session= Depends(get_db),current_user: schemas.LoginBase =Depends(get_current_user)):
     if not request.image_url_type in image_url_types:
         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,detail="Parameter image_url_type can only take value absolute and relative")
     return create(request=request, db= db)
 
 
@router.get("/all",response_model=List[schemas.PostDisplay])
def posts(db: Session= Depends(get_db)):
    return get_posts(db=db)



@router.post("/image")
def upload_image(image:UploadFile= File(...),current_user: schemas.LoginBase =Depends(get_current_user)):
    letters=string.ascii_letters
    rand_str = ''.join(random.choice(letters) for i in range(8))
    new = f'_{rand_str}.'
    filename = new.join(image.filename.rsplit('.',1))
    path = f'images/post/{filename}'

    with open(path, "w+b") as buffer:
        shutil.copyfileobj(image.file,buffer)
        
    return {'filename': path}    



@router.get("/delete/{id}")
def delete_post(id: int, db: Session = Depends(get_db), current_user: schemas.LoginBase =Depends(get_current_user)):
    return delete( db=db,id=id, user_id=current_user.id)