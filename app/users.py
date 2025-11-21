from fastapi import Depends,HTTPException,status,FastAPI,Response,APIRouter
from .database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session
from typing import Optional,List
from . import models , schemas
from . import utils

router = APIRouter(
    prefix="/user",
    tags=["Users"]
)

@router.post('/create')
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # Check for existing user (good practice)
    existing_user = db.query(models.User).filter(models.User.email == user.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"User with email '{user.email}' already exists"
        )
    hashed_password = utils.hash(user.password)

    user_data = user.model_dump()
    
    user_data['password'] = hashed_password

    new_user = models.User(**user_data)
    
    # 5. Database operations
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # The UserOut schema filters out the long hash for a secure response.
    return new_user

@router.get('/{user_id}',response_model=schemas.UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
   
   user = db.query(models.User).filter(models.User.id == user_id).first()

   if not user:
      raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with {user_id} not found')
   
   return user
   