from fastapi import FastAPI,HTTPException,status,Depends,Response
from fastapi.params import Body,Optional
from pydantic import BaseModel
from passlib.context import CryptContext
from random import randrange
from .import models
from . import utils
from .database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session
from . import schemas
from . import posts,users,auth,vote
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*'],
)

# FastAPI with having list as a database

# my_posts = [{'title':'Tutorial 1' ,'content': 'FastAPI' ,'id':1},{'title':'Tutorial 2' ,'content': 'pydantic' ,'id':2}]


# @app.get("/")
# def get_posts():
#     return {"data": my_posts}

# @app.post("/posts",status_code=status.HTTP_201_CREATED)
# def create_post(new_post:Post,):
#     if new_post:
#         new_post = new_post.dict()
#         new_post['id'] = randrange(0,10000)

#         my_posts.append(new_post)
#         return {'message': 'post created successfuly' ,'all_posts':my_posts}
#     else:
#         raise HTTPException(402,'Error occured')
    

# def findPost(id:int):
#     for i , p in enumerate(my_posts):
#         if id == p["id"]:
#             return i
        
#     return None


# @app.put('/update/{id}',status_code=status.HTTP_404_NOT_FOUND)
# def update_post(id:int , new_post: Post):
#     index = findPost(id)
    
#     if index:
#         new_post = new_post.dict()
#         new_post['id'] = id
#         my_posts[index] = new_post

#         return {'message': 'Post updated successfully', 'all_posts': my_posts}
    
#     raise HTTPException(status_code=404,detail='Post not found')
        

# @app.delete('/delete/{id}')
# def delete_post(id:int):
#     i = findPost(id)

#     if i:
#        post = my_posts.pop(i)
#        return {'message': 'Post delete successfully' , 'post': post}

#     raise HTTPException(status_code=404,detail='Post not found')

# @app.get('/latest')
# def get_latest():

#     return my_posts[len(my_posts) - 1]


# Connecting FastAPI with SQLAlchemy 

models.Base.metadata.create_all(bind=engine)


app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(vote.router)
