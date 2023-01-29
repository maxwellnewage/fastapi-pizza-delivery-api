from fastapi import APIRouter, Depends, status
from models import User, Order
from schemas import OrderModel
from auth_manager import oauth2_scheme, get_payload
from database import Session, engine
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
)

session = Session(bind=engine)


@order_router.get('/')
async def get_all_orders(token: str = Depends(oauth2_scheme)):
    user_payload = get_payload(token)

    user = session.query(User).filter(User.username == user_payload).first()

    if user.is_staff:
        orders = session.query(Order).all()
        return orders

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser")


@order_router.post('/order', status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, token: str = Depends(oauth2_scheme)):
    user_payload = get_payload(token)

    user = session.query(User).filter(User.username == user_payload).first()

    new_order = Order(
        pizza_size=order.pizza_size,
        quantity=order.quantity,
    )

    new_order.user = user

    session.add(new_order)
    session.commit()

    response = {
        "id": new_order.id,
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "order_status": new_order.order_status
    }

    return jsonable_encoder(response)