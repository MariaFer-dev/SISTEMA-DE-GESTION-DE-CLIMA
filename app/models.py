from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    favorite_cities = relationship("FavoriteCity", back_populates="user", cascade="all, delete-orphan")
    weather_history = relationship("WeatherHistory", back_populates="user", cascade="all, delete-orphan")

class FavoriteCity(Base):
    __tablename__ = "favorite_cities"
    
    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String, nullable=False)
    country_code = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relaciones
    user = relationship("User", back_populates="favorite_cities")

class WeatherHistory(Base):
    __tablename__ = "weather_history"
    
    id = Column(Integer, primary_key=True, index=True)
    city_name = Column(String, nullable=False)
    temperature = Column(Float)
    description = Column(String)
    humidity = Column(Integer)
    wind_speed = Column(Float)
    searched_at = Column(DateTime(timezone=True), server_default=func.now())
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    
    # Relaciones
    user = relationship("User", back_populates="weather_history")