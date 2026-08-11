from contextlib import asynccontextmanager

from fastapi import FastAPI

import app.handler.handler  # noqa: F401
from app.bot.bot import bot
from app.config import settings
from app.routes.routes import setup_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    webhook_path = f"/webhook/{settings.tg_bot_token.get_secret_value()}"
    if settings.webhook_url:
        await bot.set_webhook(
            url=f"{settings.webhook_url}{webhook_path}",
            drop_pending_updates=True,
        )
    yield
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.session.close()


app = FastAPI(lifespan=lifespan)
setup_routes(app)