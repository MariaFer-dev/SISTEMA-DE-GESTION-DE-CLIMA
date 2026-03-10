from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
from . import models, schemas, auth, weather
from .database import engine, get_db
from .config import settings
from app.database import SessionLocal
from sqlalchemy.sql import text

# Crear tablas en la base de datos
models.Base.metadata.create_all(bind=engine)

# Inicializar FastAPI
app = FastAPI(
    title="Sistema de Gestión de Clima con Favoritos",
    description="API para consultar clima y guardar ciudades favoritas",
    version="1.0.0"
)

# Instancia del servicio de clima
weather_service = weather.WeatherService()

# ============ RUTAS PÚBLICAS ============

@app.post("/register", response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Registra un nuevo usuario en el sistema
    """
    # Verificar si el usuario ya existe
    db_user = db.query(models.User).filter(
        (models.User.username == user.username) | (models.User.email == user.email)
    ).first()
    
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario o email ya está registrado"
        )
    
    # Crear nuevo usuario
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@app.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    Autentica un usuario y devuelve un token JWT
    """
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

# ============ RUTAS PROTEGIDAS ============

@app.get("/users/me", response_model=schemas.UserResponse)
async def read_users_me(current_user: models.User = Depends(auth.get_current_active_user)):
    """
    Obtiene la información del usuario autenticado
    """
    return current_user

@app.post("/weather/current", response_model=schemas.WeatherResponse)
async def get_current_weather(
    weather_request: schemas.WeatherRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Consulta el clima actual de una ciudad y guarda en el historial
    """
    # Obtener clima de la API externa
    weather_data = weather_service.get_current_weather(weather_request.city)
    
    # Guardar en historial
    weather_history = models.WeatherHistory(
        city_name=weather_data["city"],
        temperature=weather_data["temperature"],
        description=weather_data["description"],
        humidity=weather_data["humidity"],
        wind_speed=weather_data["wind_speed"],
        user_id=current_user.id
    )
    
    db.add(weather_history)
    db.commit()
    
    # Preparar respuesta
    response = schemas.WeatherResponse(
        city=weather_data["city"],
        temperature=weather_data["temperature"],
        description=weather_data["description"],
        humidity=weather_data["humidity"],
        wind_speed=weather_data["wind_speed"],
        feels_like=weather_data["feels_like"],
        searched_at=weather_history.searched_at
    )
    
    return response

@app.post("/favorites", response_model=schemas.FavoriteCityResponse, status_code=status.HTTP_201_CREATED)
async def add_favorite_city(
    favorite: schemas.FavoriteCityCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Agrega una ciudad a favoritos del usuario
    """
    # Verificar si ya existe
    existing = db.query(models.FavoriteCity).filter(
        models.FavoriteCity.user_id == current_user.id,
        models.FavoriteCity.city_name == favorite.city_name
    ).first()
    
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Esta ciudad ya está en tus favoritos"
        )
    
    # Crear nuevo favorito
    db_favorite = models.FavoriteCity(
        city_name=favorite.city_name,
        country_code=favorite.country_code,
        user_id=current_user.id
    )
    
    db.add(db_favorite)
    db.commit()
    db.refresh(db_favorite)
    
    return db_favorite

@app.get("/favorites", response_model=List[schemas.FavoriteCityResponse])
async def get_favorite_cities(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Obtiene todas las ciudades favoritas del usuario
    """
    favorites = db.query(models.FavoriteCity).filter(
        models.FavoriteCity.user_id == current_user.id
    ).all()
    
    return favorites

@app.delete("/favorites/{city_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_favorite_city(
    city_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Elimina una ciudad de favoritos
    """
    favorite = db.query(models.FavoriteCity).filter(
        models.FavoriteCity.id == city_id,
        models.FavoriteCity.user_id == current_user.id
    ).first()
    
    if not favorite:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ciudad favorita no encontrada"
        )
    
    db.delete(favorite)
    db.commit()

@app.get("/history", response_model=List[schemas.WeatherHistoryResponse])
async def get_weather_history(
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Obtiene el historial de consultas de clima del usuario
    """
    history = db.query(models.WeatherHistory).filter(
        models.WeatherHistory.user_id == current_user.id
    ).order_by(
        models.WeatherHistory.searched_at.desc()
    ).offset(skip).limit(limit).all()
    
    return history

@app.get("/favorites/weather")
async def get_weather_for_favorites(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(auth.get_current_active_user)
):
    """
    Obtiene el clima actual para todas las ciudades favoritas del usuario
    """
    favorites = db.query(models.FavoriteCity).filter(
        models.FavoriteCity.user_id == current_user.id
    ).all()
    
    weather_results = []
    for favorite in favorites:
        try:
            weather_data = weather_service.get_current_weather(favorite.city_name)
            weather_results.append({
                "city": favorite.city_name,
                "country_code": favorite.country_code,
                "weather": weather_data
            })
        except Exception as e:
            # Si falla una ciudad, continuar con las demás
            weather_results.append({
                "city": favorite.city_name,
                "country_code": favorite.country_code,
                "weather": None,
                "error": f"No se pudo obtener el clima: {str(e)}"
            })
    
    return weather_results

@app.get("/")
async def root():
    """
    Ruta raíz con información básica de la API
    """
    return {
        "message": "Bienvenido al Sistema de Gestión de Clima con Favoritos",
        "documentation": "/docs",
        "version": "1.0.0"
    }

def test_db_connection():
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))  # Ejecuta una consulta simple para probar la conexión
        print("Conexión a la base de datos exitosa.")
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    test_db_connection()