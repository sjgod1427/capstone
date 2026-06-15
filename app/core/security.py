from jose import JWTError, jwt
import hashlib
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.core.config import Settings


def create_access_token(data:dict , exp_time:int=30):
    to_encode=data.copy()
    expire=datetime.utcnow() + timedelta(minutes=exp_time)
    to_encode.update({'exp':expire})    
    encoded_jwt=jwt.encode(to_encode, Settings.JWT_SECRET_KEY, algorithm=Settings.JWT_ALGORITHM)
    return encoded_jwt


def verify_token(token:str):
    try:
        payload = jwt.decode(token, Settings.JWT_SECRET_KEY, algorithms=[Settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')

