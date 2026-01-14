import requests
from langchain.tools import tool
from dotenv import load_dotenv
import os

load_dotenv()
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

def geocode_city(
    city: str,
    country: str | None = None,
    limit: int = 1
) -> tuple[float, float]:
    """
    Convert city name to (lat, lon) using OpenWeather Geocoding API.
    """
    location = ",".join(filter(None, [city, country]))

    url = (
        "http://api.openweathermap.org/geo/1.0/direct"
        f"?q={location}&limit={limit}&appid={WEATHER_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if not data:
        raise ValueError(f"Could not geocode location: {location}")

    lat = data[0]["lat"]
    lon = data[0]["lon"]
    return lat, lon

def get_weather_by_coords(lat: float, lon: float) -> str:
    """
    Get current weather using latitude and longitude.
    """
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&units=metric&appid={WEATHER_API_KEY}"
    )

    response = requests.get(url)
    data = response.json()

    if data.get("weather") and data.get("main"):
        description = data["weather"][0]["description"]
        temp = data["main"]["temp"]
        return f"{description}, {temp}°C"
    else:
        raise ValueError("Invalid weather response")

@tool
def get_weather(city: str, country: str = "TW") -> str:
    """
    Get current weather for a city using OpenWeather geocoding and weather APIs.
    """
    lat, lon = geocode_city(city, country)
    return get_weather_by_coords(lat, lon)

