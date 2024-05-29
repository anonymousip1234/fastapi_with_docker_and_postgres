from typing import List,Annotated
from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas import *
from models import *
from databases import *
from .paths import *
from utils.authenticate import create_password_hash,authenticate_user,create_access_token,get_current_user

authentication_router = APIRouter()

#User Registration Api
@authentication_router.post(REGISTER,response_model=UserResponse,tags=['authentication'])
def register(request:UserRequest,db : Session = Depends(get_db)):
    hashed_password = create_password_hash(request.password)
    user = Users(email=request.email,username=request.username,password=hashed_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

#Login Api
@authentication_router.post(LOGIN,tags=["authentication"])
def login_and_create_access_token(request: Annotated[OAuth2PasswordRequestForm,Depends()],db:Session = Depends(get_db)) -> Token: 
    user = authenticate_user(db,request.username,request.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub":request.username})

    return Token(token=access_token,token_type='bearer')