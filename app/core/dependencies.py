from fastapi import HTTPException , Header
from app.core.config import Settings
from app.core.security import verify_token


def get_api_key(api_key:str=Header(None)):
    if not api_key or api_key != Settings.API_KEY:
        raise HTTPException(status_code=403, detail='Invalid API Key')
    

def get_current_user(token:str=Header(...)):
    payload= verify_token(token)
    if not payload:
        raise HTTPException(status_code=401, detail='Invalid Token')
    return payload.get('sub')  
    