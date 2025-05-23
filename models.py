from database import Base
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text
from sqlalchemy.orm import relationship
from sqlalchemy_utils import ChoiceType


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(25), unique=True, index=True, nullable=False)
    email = Column(String(50), unique=True, index=True, nullable=False)
    password = Column(Text, nullable= True)
    is_staff = Column(Boolean, default= False)
    is_active = Column(Boolean, default= False)
    orders = relationship('Order', back_populates = 'user')


    def __repr__(self):
        return f"User {self.username}"
    

class Order(Base):
    __tablename__ = "orders"

    ORDER_STATUS = (
        ('PENDING', 'pending'),
        ('in-transit', 'IN-TRANSIT'),
        ('delivered', 'DELIVERED')
    )

    PIZZAS_SIZES =( ( 'SMALL', 'small'), ('LARGE', 'large'), ('medium', 'MEDIUM')) 

    id = Column(Integer, primary_key=True, index=True)
    quantity = Column(Integer, index=True, nullable= False)
    order_status = Column(ChoiceType(choices = ORDER_STATUS), default= "PENDING")
    pizza_size = Column(ChoiceType(choices=PIZZAS_SIZES), default="small")
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship('User', back_populates='orders')


    def __repr__(self):
        return f"Order {self.id}"




