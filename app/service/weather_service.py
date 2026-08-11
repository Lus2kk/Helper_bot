from app.external.weather_client import WeatherClient

class WeatherService():
    def __init__(self, client: WeatherClient):
        self.client = client

    async def get_weather_service(self, lat: float, lon: float) -> str:
        data = await self.client.get_weather(lat=lat, lon=lon)
        current = data["current"]
        temperature = current["temperature_2m"]
        wind = current["wind_speed_10m"]
        return f"Погода: {temperature}°C, ветер {wind} м/с"
