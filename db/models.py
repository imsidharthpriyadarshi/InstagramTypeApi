from db.database import Base
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql import func

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key = True, index = True)
    username = Column(String,nullable= False,unique = True)
    email= Column(String, nullable = False,unique = True)
    password = Column(String, nullable = False)
    
    profile_photo= Column(String, server_default= "images/user/default.jpg")
    
    items = relationship('DbPost', back_populates= 'user')
    
    
    
class DbPost(Base):
    __tablename__= 'posts'
    id  = Column(Integer, primary_key= True,index = True)
    image_url = Column(String)
    image_url_type= Column(String)
    caption= Column(String)
    timestamp = Column(TIMESTAMP(timezone=True),nullable= False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey('users.id',ondelete='CASCADE'),nullable= False)
    
    user = relationship('DbUser', back_populates= 'items')
    comments =relationship("DbComment", back_populates= 'post')
    
class DbComment(Base):
    __tablename__ = 'comment'
    id = Column(Integer, primary_key= True, index= True)
    text = Column(String,nullable= False)
    username = Column(String,nullable= False)
    created_at = Column(TIMESTAMP(timezone=True),nullable= False,server_default=func.now())
    
    post_id = Column(Integer,ForeignKey('posts.id',ondelete='CASCADE'),nullable= False)
    
    post = relationship("DbPost", back_populates= 'comments')