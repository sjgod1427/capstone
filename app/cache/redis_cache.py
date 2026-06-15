import json 
import redis
from app.core.config import Settings


reduis_client = redis.Redis(host=Settings.REDIS_HOST, port=Settings.REDIS_PORT, db=Settings.REDIS_DB)

def get_cached_prediction(key:str):
    cached = reduis_client.get(key)
    if cached:
        return json.loads(cached)
    return None

def set_cached_prediction(key:str, value:dict, expiry:int=3600):
    reduis_client.set(key, json.dumps(value), ex=expiry)