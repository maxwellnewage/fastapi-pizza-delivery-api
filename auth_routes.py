from fastapi import APIRouter, status
from database import Session, engine
from schemas import SignUpModel, LoginModel
from models import User
from fastapi.exceptions import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash
from jose import jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta

ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET_KEY = 'bda3db1e23c619aa4f6ebb4d9398d5535b999a6e364eed6fcef526c4e1ee5cb2'

crypt = CryptContext(schemes=["bcrypt"])

auth_router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

session = Session(bind=engine)


@auth_router.get('/')
async def hello():
    return {"message": "Hello auth"}


@auth_router.post('/signup', response_model=SignUpModel, status_code=status.HTTP_201_CREATED)
async def signup(user: SignUpModel):
    db_username = session.query(User).filter(User.email == user.email or User.username == user.username).first()

    if db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password= generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )

    session.add(new_user)
    session.commit()

    return new_user


@auth_router.post('/login')
async def login(user: LoginModel):
    db_user = session.query(User).filter(User.username == user.username).first()

    if db_user and check_password_hash(db_user.password, user.password):
        access_token = {
            "sub": db_user.username,
            "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)
        }

        return {
            'access_token': jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
        }

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Invalid user or password"
    )
