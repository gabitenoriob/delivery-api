from fastapi import FastAPI
from routes.auth_routes import auth_router
from openai import models
from routes.order_routes import order_router
from database import engine, get_db

app = FastAPI()
app.include_router(auth_router)
app.include_router(order_router)




