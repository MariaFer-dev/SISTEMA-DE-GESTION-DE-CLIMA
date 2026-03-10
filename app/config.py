from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./test.db"
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    OPENWEATHER_API_KEY: str = "e53d43ff63a5faccd746b94f92d78044"  
    OPENWEATHER_BASE_URL: str = "https://api.openweathermap.org/data/2.5"
    
    class Config:
        env_file = ".env"

settings = Settings()