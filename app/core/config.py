import os
from dotenv import load_dotenv

load_dotenv()



class Settings:
    project_name: str = "Car Price API"
    API_KEY: str = os.getenv("API_KEY")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = "HS256"
    REDIS_URL: str = os.getenv("REDIS_URL")
    MODEL_PATH: str = 'app/models/car_price_model.pkl'

settings = Settings()