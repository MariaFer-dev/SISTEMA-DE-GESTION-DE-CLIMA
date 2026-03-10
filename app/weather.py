import requests
from fastapi import HTTPException
from app.config import settings

class WeatherService:
    def __init__(self):
        self.api_key = settings.OPENWEATHER_API_KEY
        self.base_url = settings.OPENWEATHER_BASE_URL
    
    def get_current_weather(self, city: str):
        """Obtiene el clima actual de una ciudad desde OpenWeatherMap"""
        try:
            # Construir URL para clima actual
            url = f"{self.base_url}/weather"
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric",  # Para temperatura en Celsius
                "lang": "es"  # Descripciones en español
            }
            
            # Hacer la petición
            response = requests.get(url, params=params)
            
            # Verificar si hubo error
            if response.status_code != 200:
                error_data = response.json()
                raise HTTPException(
                    status_code=response.status_code,
                    detail=f"Error de OpenWeatherMap: {error_data.get('message', 'Ciudad no encontrada')}"
                )
            
            # Procesar respuesta exitosa
            data = response.json()
            
            weather_info = {
                "city": data["name"],
                "temperature": data["main"]["temp"],
                "description": data["weather"][0]["description"],
                "humidity": data["main"]["humidity"],
                "wind_speed": data["wind"]["speed"],
                "feels_like": data["main"]["feels_like"]
            }
            
            return weather_info
            
        except requests.RequestException as e:
            raise HTTPException(
                status_code=503,
                detail=f"Error de conexión con el servicio de clima: {str(e)}"
            )