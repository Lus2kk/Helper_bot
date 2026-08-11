from app.external.news_client import NewsClient


class NewsService:
    def __init__(self, client: NewsClient):
        self.client = client

    async def get_news(self, topic: str) -> list[dict]:
        data = await self.client.get_news(topic=topic, lang="ru", max_results=5)
        articles = data.get("articles", [])
        return [
            {
                "title": a.get("title", ""),
                "description": a.get("description", ""),
                "image": a.get("image"),
                "url": a.get("url", ""),
            }
            for a in articles
        ]