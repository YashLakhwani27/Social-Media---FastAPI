from jose import JWTError,jwt
from datetime import datetime,timedelta
from . import schemas,database,models
from fastapi import Depends,status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/login')

SECRET_KEY = setting.SECRET_KEY
ALGORITHM = setting.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = setting.ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):

    encode_data = data.copy()

    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    encode_data.update({"exp": expire})
    encoded_jwt = jwt.encode(encode_data,SECRET_KEY,algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str,credentials_exception):
    try:

        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id: str = (payload.get("id"))

        if id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exception

    return token_data

def get_current_user(token: str = Depends(oauth2_scheme),db: Session = Depends(database.get_db)):

    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Could not verify credentials",headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token,credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
    