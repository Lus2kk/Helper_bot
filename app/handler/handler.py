from pathlib import Path
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, CallbackQuery
from app.bot.bot import bot, dp
from app.external.weather_client import WeatherClient
from app.external.news_client import NewsClient
from app.service.weather_service import WeatherService
from app.service.news_service import NewsService
from aiogram.utils.keyboard import InlineKeyboardBuilder


weather_service = WeatherService(WeatherClient())
news_service = NewsService(NewsClient())


welcome_text = (Path(__file__).parent.parent / "bot" / "text" / "welcome.txt").read_text(encoding="utf-8")


@dp.message(CommandStart())
async def start_command_handler(message: Message):
    await message.answer(welcome_text)

help_text = (Path(__file__).parent.parent / "bot" / "text" / "help.txt").read_text(encoding="utf-8")


@dp.message(Command("help"))
async def help_command_handler(message: Message):
    await message.answer(help_text)


location_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Поделиться геолокацией", request_location=True)]],
    resize_keyboard=True,
)


@dp.message(Command("weather"))
async def weather_command_handler(message: Message):
    await message.answer(
        "Для того чтобы я мог сказать тебе погоду в твоей точке, мне надо твоя геолокация",
        reply_markup=location_keyboard,
    )


@dp.message(lambda m: m.location is not None)
async def location_handler(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude
    try:
        text = await weather_service.get_weather_service(lat=lat, lon=lon)
        await message.answer(text, reply_markup=ReplyKeyboardRemove())
    except Exception:
        await message.answer(
            "Не удалось получить погоду. Попробуй позже.",
            reply_markup=ReplyKeyboardRemove(),
        )


NEWS_TOPICS = {
    "sports": "Спорт",
    "technology": "Технологии",
    "entertainment": "Кино",
    "business": "Бизнес",
    "science": "Наука",
    "world": "Мир",
    "health": "Здоровье",
}


def news_keyboard():
    builder = InlineKeyboardBuilder()
    for topic_key, topic_label in NEWS_TOPICS.items():
        builder.button(text=topic_label, callback_data=f"news:{topic_key}")
    builder.adjust(2)
    return builder.as_markup()


@dp.message(Command("news"))
async def news_command_handler(message: Message):
    await message.answer("Выбери тему новостей:", reply_markup=news_keyboard())


@dp.callback_query(lambda c: c.data and c.data.startswith("news:"))
async def news_callback_handler(callback: CallbackQuery):
    topic = callback.data.split(":")[1]
    topic_label = NEWS_TOPICS.get(topic, topic)
    await callback.answer(f"Загружаю: {topic_label}")
    try:
        articles = await news_service.get_news(topic=topic)
        if not articles:
            await callback.message.answer("Нет новостей по этой теме.")
            return
        first = articles[0]
        caption = f"{first['title']}\n\n{first['description']}\n\nЧитать: {first['url']}"
        if first["image"]:
            if len(caption) > 1024:
                caption = caption[:1021] + "..."
            await bot.send_photo(
                chat_id=callback.message.chat.id,
                photo=first["image"],
                caption=caption,
            )
        else:
            await callback.message.answer(caption)
        rest = "\n\n".join(
            f"{a['title']}\n{a['url']}" for a in articles[1:]
        )
        if rest:
            await callback.message.answer(f"Ещё новости:\n\n{rest}")
    except Exception:
        await callback.message.answer("Не удалось получить новости. Попробуй позже.")


#