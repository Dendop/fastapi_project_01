from pydantic import BaseModel, EmailStr, conint
from typing import Optional, Literal
from datetime import datetime


class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True
    
class UserMsg(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        from_attributes = True
    
    
class CreatePost(PostBase): #inherits attributes from PostBase
    user : str #this is additional attribute only CreatePost has
    user_id : int
    
class ResponsePost(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    
    class Config:
        from_attributes = True
        
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    

        
class UserLogin(BaseModel):
    email: EmailStr
    password : str
    
class Token(BaseModel):
    access_token: str
    token_type : str
    
class TokenData(BaseModel):
    id : Optional[int] = None
    
class Vote(BaseModel):
    post_id: int
    dir : Literal[0,1]
    
class PostOut(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    user_id : int
    class Config:
        from_attributes = True

class PostWithVotes(BaseModel):
    post: PostOut
    votes: int