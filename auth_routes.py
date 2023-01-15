from fastapi import APIRouter, status
from database import Session, engine
from schemas import SignUpModel
from models import User
from fastapi import HTTPException
from werkzeug.security import generate_password_hash, check_password_hash


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
    db_email = session.query(User).filter(User.email == user.email).first()
    db_username = session.query(User).filter(User.username == user.username).first()

    if db_email is not None or db_username is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=generate_password_hash(user.password),
        is_active=user.is_active,
        is_staff=user.is_staff,
    )

    session.add(new_user)
    session.commit()

    return new_user
