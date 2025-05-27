from fastapi import APIRouter, Depends, HTTPException
from database import SessionLocal,engine, get_db, Base
from grpc import Status
from models import User
from schemas import SignUpModel
from sqlalchemy.orm import sessionmaker, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
from fastapi_jwt_auth import AuthJWT
from schemas import LoginModel
from fastapi.encoders import jsonable_encoder

auth_router = APIRouter(prefix= '/auth', tags= ['auth'])
session = SessionLocal(bind=engine)
@auth_router.get('/')
async def hello():
    return "hello"

@auth_router.post('/sign-up', response_model=SignUpModel, status_code=Status.HTTP_201_CREATED)
async def sign_up(user: SignUpModel):
    db_email = session.query(User).filter(User.email == user.email).first()
    if db_email:
        raise HTTPException(status_code=Status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    db_username = session.query(User).filter(User.username == user.username).first()
    if db_username:
        raise HTTPException(status_code=Status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    
    user.password = generate_password_hash(user.password, method='sha256')
    new_user = User(**user.model_dump())
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@auth_router.post('/login')
async def login(user: LoginModel, Authorize: AuthJWT = Depends()):
    db_user = session.query(User).filter(User.username == user.username).first()
    if db_user and check_password_hash(db_user.password,user.password):
        acess_token = Authorize.create_access_token(subject=db_user.username)
        refresh_token = Authorize.create_refresh_token(subject= db_user.username)

        response = {
            "acess": acess_token,
            "refresh": refresh_token
        }
    
        return jsonable_encoder(response)

    raise HTTPException(status_code=Status.HTTP_400_BAD_REQUEST, detail= "Invalid username or password")
    

