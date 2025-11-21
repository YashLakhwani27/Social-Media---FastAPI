from fastapi import FastAPI,HTTPException,status
from fastapi.params import Body,Optional
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
import time

class Post(BaseModel):
    title: str
    content: str 
    published: bool

app = FastAPI()

while True:
    try:
        conn = psycopg2.connect(host='localhost',database='FastAPi',user='postgres',password='yashu@271609',cursor_factory=RealDictCursor) # cursor_factory used for mapping with the Column
        cursor = conn.cursor()

        print("Database connected successfully")
        break
    except Exception as e:
        print("Something went wrong error: " ,e)
    time.sleep(2)

my_posts = [{'title':'Tutorial 1' ,'content': 'FastAPI' ,'id':1},{'title':'Tutorial 2' ,'content': 'pydantic' ,'id':2}]


@app.get("/")
def get_posts():

    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    print(posts)
    return {"data": posts}

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_post(new_post:Post,):

   cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s ,%s) RETURNING * """,(new_post.title,new_post.content,new_post.published))
   post = cursor.fetchone()

   print(post)
   if post == None:
       raise HTTPException(status_code=404,detail="Post not created")
   
   conn.commit()

   return {'new_post': post}
   

@app.get('/find/{id}')
def findPost(id : int):

    cursor.execute("""SELECT * FROM posts WHERE id = %s """,(str(id)))
    post = cursor.fetchone()
    print(post)

    if post == None:
        raise HTTPException(status_code=404,detail="Post not found")
    
    return {"post": post}

@app.delete('/delete/{id}')
def delete_post(id: int):

    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """,(str(id)))
    post = cursor.fetchone()
    conn.commit()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    
    return {'post': post}
    
@app.put('/update/{id}')
def update_post(id: int,updated_post:Post):

    cursor.execute("""UPDATE posts SET title = %s ,content = %s , published = %s  WHERE id = %s RETURNING * """,(updated_post.title,updated_post.content,updated_post.published,str(id)))

    new_post = cursor.fetchone()

    conn.commit()
    
    print(new_post)
    if new_post == None:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Post not found")
    
    return {"updated post": new_post}