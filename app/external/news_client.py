import httpx

from app.config import settings


class NewsClient:
    def __init__(self):
        self.base_url = settings.gnews_api_url
        self.api_key = settings.gnews_api_key.get_secret_value()
        self.client = httpx.AsyncClient()

    async def get_news(self, topic: str, lang: str = "ru", max_results: int = 5) -> dict:
        params = {
            "topic": topic,
            "lang": lang,
            "max": max_results,
            "apikey": self.api_key,
        }
        response = await self.client.get(f"{self.base_url}/api/v4/top-headlines", params=params)
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()