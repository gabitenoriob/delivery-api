from fastapi import FastAPI
from routes.auth_routes import auth_router
from openai import models
from routes.order_routes import order_router
import models 
from database import engine, get_db, Base 

# Ela dirá ao SQLAlchemy para criar todas as tabelas definidas em seus modelos
models.Base.metadata.create_all(bind=engine)


app = FastAPI()
app.include_router(auth_router)
app.include_router(order_router)




