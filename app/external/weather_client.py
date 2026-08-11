from app.config import settings
import httpx


class WeatherClient:
    def __init__(self):
        self.base_url = settings.open_meteo_api_url
        self.client = httpx.AsyncClient()

    async def get_weather(self, lat: float, lon: float) -> dict:
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,wind_speed_10m,precipitation,weather_code,"
        }
        response = await self.client.get(f"{self.base_url}/v1/forecast", params=params)
        response.raise_for_status()
        return response.json()