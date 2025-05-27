from typing import Optional
from pydantic import BaseModel, Field
from sqlalchemy import false, true

class SignUpModel(BaseModel):
    id: Optional[int]
    username : str
    email : str
    password : str
    is_active : Optional[bool] 
    is_staff : Optional[bool] 


    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "john_doe",
                "email": "john_doe@example.com",
                "password": "securepassword",
                "is_active": True,
                "is_staff": False
            }
        }

class Settings(BaseModel):
    auth_jwt_secret_key: str = '65b580a08e4f362f64174e9b5d0259fe5210594ed355b5c680e7f2ab260f6ea9' #gerado pelo python secrets.hex()

class LoginModel(BaseModel):
    username: str
    password: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "username": "john_doe",
                "password": "securepassword"
            }
        }