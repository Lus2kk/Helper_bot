from aiogram import Dispatcher, Bot
from app.config import settings


bot = Bot(token=settings.tg_bot_token.get_secret_value())
dp = Dispatcher()


