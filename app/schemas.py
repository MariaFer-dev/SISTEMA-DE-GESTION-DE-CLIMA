from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

# Esquemas para Usuario
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Esquemas para Token
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# Esquemas para Ciudades Favoritas
class FavoriteCityBase(BaseModel):
    city_name: str
    country_code: Optional[str] = None

class FavoriteCityCreate(FavoriteCityBase):
    pass

class FavoriteCityResponse(FavoriteCityBase):
    id: int
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Esquemas para Clima
class WeatherRequest(BaseModel):
    city: str

class WeatherResponse(BaseModel):
    city: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    feels_like: float
    searched_at: datetime

class WeatherHistoryResponse(BaseModel):
    id: int
    city_name: str
    temperature: float
    description: str
    humidity: int
    wind_speed: float
    searched_at: datetime
    
    class Config:
        from_attributes = True