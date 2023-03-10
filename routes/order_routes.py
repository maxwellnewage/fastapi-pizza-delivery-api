from fastapi import APIRouter, Depends, status
from models import User, Order
from schemas import OrderModel
from auth_manager import oauth2_scheme, get_payload
from database.globals import Session, engine
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import HTTPException

order_router = APIRouter(
    prefix='/orders',
    tags=['orders']
)

session = Session(bind=engine)


def get_user(token: str):
    """
    Obtiene usuario en base al token por oauth
    :param token:
    :return: User
    """
    user_payload = get_payload(token)
    return session.query(User).filter(User.username == user_payload).first()


def is_admin(user):
    """
    Comprueba si el usuario es administrador (is_staff == True)
    :param user:
    :return: True | HTTPException
    """
    if user.is_staff:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser")


@order_router.get('/')
async def get_all_orders(token: str = Depends(oauth2_scheme)):
    """
    Obtiene todas las ordenes
    :param token:
    :return: List[Order]
    """
    user = get_user(token)

    if is_admin(user):
        orders = session.query(Order).all()
        return orders


@order_router.post('/', status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderModel, token: str = Depends(oauth2_scheme)):
    """
    Crea una orden nueva y la retorna
    :param order:
    :param token:
    :return: Order
    """
    user = get_user(token)

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


@order_router.get('/{order_id}')
async def get_order(order_id: int, token: str = Depends(oauth2_scheme)):
    """
    Obtiene una orden seg??n el Id
    :param order_id:
    :param token:
    :return: Order
    """
    user = get_user(token)

    if is_admin(user):
        return session.query(Order).filter(Order.id == order_id).first()


@order_router.get('/user/all')
async def get_user_orders(token: str = Depends(oauth2_scheme)):
    """
    Obtiene las ??rdenes que hizo el usuario autenticado
    :param token:
    :return: List[Order]
    """
    user = get_user(token)

    return session.query(User).filter(User.username == user.username).first().orders


@order_router.put('/{order_id}')
async def update_order(order_id: int, order: OrderModel, token: str = Depends(oauth2_scheme)):
    """
    Actualiza una orden existente
    :param order_id:
    :param order:
    :param token:
    :return: Order
    """
    user = get_user(token)
    order_bd = session.query(Order).filter(Order.id == order_id and Order.user.username == user).first()

    order_bd.quantity = order.quantity
    order_bd.pizza_size = order.pizza_size

    session.commit()

    return jsonable_encoder(order_bd)


@order_router.delete('/{order_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: int, token: str = Depends(oauth2_scheme)):
    """
    Elimina una orden
    :param order_id:
    :param token:
    :return: None
    """
    user = get_user(token)
    session.query(Order).filter(Order.id == order_id and Order.user.username == user).delete()

    session.commit()
