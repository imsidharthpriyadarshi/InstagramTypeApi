from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr




class UserBase(BaseModel):
    username :str
    email :EmailStr
    password: str

             
class UserDisplay(BaseModel):
    username :str
    email : EmailStr
    profile_pic:str

    class Config():
        orm_mode= True
        
        
class PostBase(BaseModel):
    caption:str
         
class PostBaseOut(BaseModel):
    caption:str
    user_id:int
    class Config():
        orm_mode= True
           
 #for post pic
class PostId(BaseModel):
    id:int 
    
class PostWithPic(PostId):
    image_url:str
    class Config():
        orm_mode= True
                    
class PostPicOut(PostId):
    image_url:str
    post_id:int
    userposts:PostBaseOut
    class Config():
        orm_mode= True
        
        

    
class User(BaseModel):
    id:int
    username: str
    profile_pic:str
    class Config():
        orm_mode= True
        
#for comment display  

class Comment(BaseModel):
    text:str  
    user_comment:UserDisplay 
    created_at: datetime  
    class Config():
        orm_mode= True
        
class PostDisplay(BaseModel):
    id:int
    caption:str
    timestamp: datetime
    user :User
    post_pics:List[PostWithPic]
    comments: List[Comment]
    class Config():
       orm_mode= True
       
       
#current user schema       
class LoginBase(BaseModel):
    id: int
    email: EmailStr
    username:str     
   
class CommentBase(BaseModel):
        text: str
        post_id:int
        

        