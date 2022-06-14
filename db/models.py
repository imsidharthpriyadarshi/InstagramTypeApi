
from db.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String,Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String,nullable= False,unique = True)
    email= Column(String, nullable = False,unique = True)
    profile_pic= Column(String, nullable= False, server_default="images/user/default.jpg")
    password = Column(String, nullable = False)
    is_verified= Column(Boolean,nullable=False,default= False)
    items = relationship('DbPost', back_populates= 'user')


    
    
class DbPost(Base):
    __tablename__= 'posts'
    id  = Column(Integer, primary_key= True,index = True)
    caption= Column(String)
    timestamp = Column(TIMESTAMP(timezone=True),nullable= False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey('users.id',ondelete='CASCADE'),nullable= False)
    
    user = relationship('DbUser', back_populates= 'items')
    comments =relationship("DbComment", back_populates= 'post')
    post_pics= relationship("DbPostPic",back_populates='userposts')
    
class DbComment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key= True, index= True)
    text = Column(String,nullable= False)
    username = Column(String,ForeignKey('users.username',ondelete='CASCADE'),nullable= False)
    created_at = Column(TIMESTAMP(timezone=True),nullable= False,server_default=func.now())
    
    post_id = Column(Integer,ForeignKey('posts.id',ondelete='CASCADE'),nullable= False)
    user_comment= relationship('DbUser')

    post = relationship("DbPost", back_populates= 'comments')
    
    
    
    


class DbPostPic(Base):
    __tablename__ = 'post_pic'
    id = Column(Integer, primary_key= True, index= True)
    image_url = Column(String)
    post_id= Column(Integer,ForeignKey('posts.id',ondelete='CASCADE'), nullable = False)
    userposts= relationship("DbPost",back_populates='post_pics')
    
    
class DbOTP(Base):
    __tablename__ = 'email_otp'
    username= Column(String, ForeignKey('users.username',ondelete='CASCADE'),primary_key=True,nullable = False)
    otp=    Column(String,nullable = False)
    