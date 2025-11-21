from fastapi import Depends,HTTPException,status,FastAPI,Response,APIRouter
from .database import engine,SessionLocal,get_db
from sqlalchemy.orm import Session
from . import models , schemas,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(
   tags=["Authentication"]
)


@router.post("/login")
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not utils.verify(form_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid Credentials")

    access_token = oauth2.create_access_token({"id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
