from jose.exceptions import JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi import status

ALGORITHM = "HS256"
TOKEN_DURATION_MINUTES = 30
SECRET_KEY = 'bda3db1e23c619aa4f6ebb4d9398d5535b999a6e364eed6fcef526c4e1ee5cb2'

crypt = CryptContext(schemes=["bcrypt"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_access_token(username: str):
    access_token = {
        "sub": username,
        "exp": datetime.utcnow() + timedelta(minutes=TOKEN_DURATION_MINUTES)
    }

    return {
        'access_token': jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM),
        "token_type": "bearer"
    }


def get_payload(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload.get("sub")
