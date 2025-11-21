from fastapi import Depends,HTTPException,status,FastAPI,Response,APIRouter
from .database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session
from typing import Optional,List
from . import models , schemas,oauth2
from sqlalchemy import func

router = APIRouter(
   tags=["Posts"]
)


@router.get('/')
def test_user():
   return {'message':'Hello World'}


@router.get("/sqlalchemy",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),limit: int = 10,skip : int = 0,search:Optional[str] = ""):
   posts = db.query(models.Post).all()

   if not posts:
       raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Posts not found')
   
   results = db.query(models.Post,func.count(models.Votes.posts_id).label("votes")).join(models.Votes,models.Votes.posts_id == models.Post.id , isouter=True).group_by(models.Post.id).all()
   
   return results


@router.post('/create',response_model=schemas.Post)
def create_post(post: schemas.PostCreate,db: Session = Depends(get_db),current_user : models.User = Depends(oauth2.get_current_user)):

   print(current_user.email)
   new_post = models.Post(owner_id=current_user.id,**post.dict())
   db.add(new_post)
   db.commit()

   db.refresh(new_post)

   return new_post

@router.delete('/delete/{id}')
def delete_post(id:int,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):

   post = db.query(models.Post).filter(id == models.Post.id).first()

   if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Posts not found')
   
   if post.owner_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized for perform this")
   
   db.delete(post)

   db.commit()

   return {'message':'Post removed successfully'}

@router.put('/update/{id}', response_model = schemas.Post)
def update_post(id:int,updated_post:schemas.PostCreate,db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if not post:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='Posts not found')
    
    if post.owner_id != current_user.id:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized for perform this")
    
    post_query.update(updated_post.dict(),synchronize_session=False)

    db.commit()

    return Response(status_code=201,content="Post updated successfully")