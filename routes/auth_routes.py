from fastapi import APIRouter, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from database.globals import Session, engine
from schemas import SignUpModel
from models import User
from fastapi.exceptions import HTTPException
from auth_manager import get_access_token, crypt


auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

session = Session(bind=engine)


@auth_router.post('/signup', response_model=SignUpModel, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    """
    Se registra un usuario nuevo, comprobando si existe en la BD
    :param user:
    :return: User
    """
    db_username = session.query(User).filter(User.email == user.email or User.username == user.username).first()

    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=crypt.hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )

    session.add(new_user)
    session.commit()

    return new_user


@auth_router.post('/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """
    Se autentica usuario y se genera un JWT
    :param form:
    :return: Json Web Token de User
    """
    user = session.query(User).filter(User.username == form.username).first()

    if user and crypt.verify(form.password, user.password):
        return get_access_token(user.username)

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid user or password"
    )
