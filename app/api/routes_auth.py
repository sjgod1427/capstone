from fastapi import APIRouter, Depends
from app.core.security import create_access_token
from app.core.dependencies import get_api_key
from pydantic import BaseModel

router = APIRouter()

class AuthInput(BaseModel):
    username: str
    password: str

@router.post('/login')
def login(auth: AuthInput):
    if auth.username=="admin" and auth.password=="admin":
        token = create_access_token({'sub':auth.username})
        return {'access_token':token}
    
    return {'error':'Invalid Credentials'}
