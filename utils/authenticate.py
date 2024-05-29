from typing import Annotated
from datetime import timedelta,datetime,timezone
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from databases import get_db
from models import Users
from schemas import TokenData,User
from databases import db

SECERET_KEY='0fd11a29aa4eeeb8120013a6970a670386a391b6d74fee3a7f0252aad9a8678c'
ALGORITHM='HS256'

pwd_context = CryptContext(schemes=['bcrypt'],deprecated='auto')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_password_hash(password):
    return pwd_context.hash(password)

def verify_password_hash(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)

def authenticate_user(db,username,password):
    user = db.query(Users).filter_by(username=username).first()

    if not user:
        return False
    if not verify_password_hash(password,user.password):
        return False
    return user

def create_access_token(data : dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp" : expire})
    encoded_jwt = jwt.encode(to_encode,SECERET_KEY,algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(token : Annotated[str,Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token,SECERET_KEY,algorithms=[ALGORITHM])
        username : str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except:
        raise credentials_exception
    
    user = db.query(Users).filter_by(username=username).first()
    if user is None:
        raise credentials_exception
    
    return user
