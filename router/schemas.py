from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr




class UserBase(BaseModel):
    username :str
    email :EmailStr
    password: str
    profile_photo:Optional[str] = None
    
class UserDisplay(BaseModel):
    username :str
    email : EmailStr
    profile_photo:str
    
    class Config():
        orm_mode= True
        
        
class PostBase(BaseModel):
    image_url:str
    image_url_type:str
    caption:str
    user_id:int
         
    
 #post display
 
class User(BaseModel):
    username: str
    profile_photo:str
    class Config():
        orm_mode= True
        
#for comment display  

class Comment(BaseModel):
    text:str
    username:str  
    created_at: datetime    
    class Config():
        orm_mode= True
        
class PostDisplay(BaseModel):
    id:int
    image_url: str
    image_url_type:str
    caption:str
    timestamp: datetime
    user :User
    comments: List[Comment]
    class Config():
       orm_mode= True
       
       
class LoginBase(BaseModel):
    id: int
    email: EmailStr
    username:str     
   
class CommentBase(BaseModel):
        username: str
        text: str
        post_id:int