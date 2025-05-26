from fastapi import APIRouter, HTTPException
from database import SessionLocal,engine, get_db, Base
from grpc import Status
from models import User
from routes.schemas import SignUpModel
from sqlalchemy.orm import sessionmaker, declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

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
