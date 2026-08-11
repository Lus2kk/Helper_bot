from aiogram.types import Update
from fastapi import APIRouter, FastAPI

from app.bot.bot import bot, dp
from app.config import settings

router = APIRouter()


@router.post(f"/webhook/{settings.tg_bot_token.get_secret_value()}")
async def webhook_endpoint(update: dict):
    telegram_update = Update(**update)
    await dp.feed_update(bot=bot, update=telegram_update)
    return {"ok": True}


@router.get("/health")
async def health_message():
    return {"message": "server is running"}


def setup_routes(app: FastAPI):
    app.include_router(router) 