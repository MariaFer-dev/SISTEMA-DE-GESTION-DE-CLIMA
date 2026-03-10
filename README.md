# 🌦️ Sistema de Gestión de Clima

Sistema backend desarrollado para consultar y gestionar información meteorológica utilizando una API de clima externa.  
El sistema permite obtener **datos climáticos en tiempo real** y exponerlos mediante **endpoints REST**.

---

# 📌 Descripción del Proyecto

**Sistema de Gestión de Clima** es una aplicación backend que permite consultar datos meteorológicos desde una API externa y gestionarlos dentro de una aplicación.

El sistema realiza solicitudes a un servicio de clima para obtener información como:

- 🌡️ Temperatura actual  
- 💧 Humedad  
- 🌬️ Velocidad del viento  
- ☁️ Condiciones climáticas

Las APIs meteorológicas permiten acceder a datos del clima global en tiempo real mediante solicitudes HTTP que devuelven información estructurada en formato **JSON**.

Este proyecto fue desarrollado como práctica de:

- Consumo de **APIs externas**
- Desarrollo de **servicios backend**
- Implementación de **endpoints REST**

---

# ⚙️ Tecnologías Utilizadas

- 🐍 Python  
- ⚡ Flask / FastAPI  
- 🔗 REST API  
- 📡 Requests  
- 📦 JSON  
- 🔐 Variables de entorno (`.env`)  
- 🌱 Git  
- 🐙 GitHub  

---

# 🚀 Instalación

## 1️⃣ Clonar el repositorio

-- bash
git clone https://github.com/MariaFer-dev/SISTEMA-DE-GESTION-DE-CLIMA.git

## 2️⃣ Entrar al proyecto 
cd SISTEMA-DE-GESTION-DE-CLIMA


## 3️⃣ Crear entorno virtual
python -m venv venv

--- Activar entorno virtual 
-Windows 
venv\Scripts\activate 
Linux / Mac 
source venv/bin/activate


## 4️⃣ Instalar dependencias
pip install -r requirements.txt


##🔑 Variables de Entorno 
Crear un archivo .env con 
la siguiente configuración: 
WEATHER_API_KEY=tu_api_key 
SECRET_KEY=tu_clave_secreta
Las claves de API permiten autenticar las solicitudes hacia el servicio meteorológico externo.
 

##▶️ Ejecutar el Proyecto
python run.py
