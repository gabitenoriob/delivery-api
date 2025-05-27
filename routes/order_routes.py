from fastapi import APIRouter
from fastapi import HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from models import Order,User
from schemas import OrderModel
from database import SessionLocal, engine, get_db, Base

order_router = APIRouter(prefix= '/orders', tags= ['orders'])

session = SessionLocal(bind=engine)

@order_router.get('/')
async def hello(Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized, invalid token")
    return "hello"

@order_router.post('/order', response_model=OrderModel, status_code=201)
async def place_an_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    try:
        Authorize.jwt_required()
    except Exception as e:
        raise HTTPException(status_code=401, detail="Unauthorized, invalid token")
    
    current_user = Authorize.get_jwt_subject()
    user = session.query(User).filter_by(username=current_user).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    new_order = Order(**order.model_dump(), user_id=user.id)
    
    session.add(new_order)
    session.commit()
    session.refresh(new_order)
    response = {"order_id": new_order.id, "message": "Order placed successfully", "order_details": new_order}
    
    return jsonable_encoder(response)