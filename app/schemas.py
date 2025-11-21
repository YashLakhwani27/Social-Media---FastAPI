from pydantic import BaseModel,Field,EmailStr
from typing import Optional,Annotated
from datetime import datetime

class PostBase(BaseModel):
    title: str
    content: str 
    published: Optional[bool] = True
    owner_id: int

class PostCreate(BaseModel):
     title: str
     content: str 
     published: Optional[bool] = True
   
class UserOut(BaseModel):
    id: int
    email: str
    created_at:datetime

    class Config:
        from_attributes = True
        
class Post(PostBase): # ------------- For response pydantic schema
    title: str
    content: str
    published: Optional[bool] = True
    created_at: datetime
    id: int
    owner_id:int
    owner: UserOut

    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(...,max_length=70)

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    type: str

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    id: Optional[int]

    class Config:
        from_attributes = True


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(le=1)]

    class Config:
        from_attributes = True