from pathlib import Path
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from app.bot.bot import bot, dp
from app.external.news_client import NewsClient
from app.external.weather_client import WeatherClient
from app.keyboards.keyboards import (
    NEWS_TOPICS,
    location_keyboard,
    main_keyboard,
    news_keyboard,
)
from app.service.news_service import NewsService
from app.service.weather_service import WeatherService


# конструкторы сервиса
weather_service = WeatherService(WeatherClient())
news_service = NewsService(NewsClient())


# приветственный текст для команды /start 
welcome_text = (Path(__file__).parent.parent / "bot" / "text" / "welcome.txt").read_text(encoding="utf-8")
# ручка для /start - возвращает текст выше
@dp.message(CommandStart())
async def start_command_handler(message: Message):
    await message.answer(welcome_text, reply_markup=main_keyboard)


# ручка для помощи пользователю, при нажатии кнопки вылетает текст из help.txt 
# который обьясняет пользователю команды бота 
help_text = (Path(__file__).parent.parent / "bot" / "text" / "help.txt").read_text(encoding="utf-8")
@dp.message(F.text == "Помощь")
async def help_command_handler(message: Message):
    await message.answer(help_text)


# обработчик нажатия кнопки "Погода" (из главного меню)
# при нажатии кнопки "Погода" отправляется запрос на получение геолокации пользователя 
# логика этого запроса прописана в следующей функции 
@dp.message(F.text == "Погода")
async def weather_button_handler(message: Message):
    await message.answer(
        "Для того чтобы я мог сказать тебе погоду в твоей точке, мне надо твоя геолокация",
        reply_markup=location_keyboard,
    )

# ручка на получение погоды через Open-meteo
# после получения координат геолокации формируется запрос в Open-meteo 
# для получения погоды в месте геолокации 
# важно учесть что использование геолокации идет строго через Telegram 
@dp.message(lambda m: m.location is not None)
async def location_handler(message: Message):
    lat = message.location.latitude
    lon = message.location.longitude
    try:
        text = await weather_service.get_weather_service(lat=lat, lon=lon)
        await message.answer(text, reply_markup=main_keyboard)
    except Exception as e:
        await message.answer(
            f"Не удалось получить погоду. Ошибка: {repr(e)}",
            reply_markup=main_keyboard,
        )


# обработчик нажатия кнопки "Новости"
# при нажатии кнопки вызывается дополнитклное окно с категориями новостей
# после чего формируется запрос в GNews исходя их query-параметра топика новостей 
# выбранного пользователем 
@dp.message(F.text == "Новости")
async def news_button_handler(message: Message):
    await message.answer("Выбери тему новостей:", reply_markup=news_keyboard())

# обработчик нажатия на inline-кнопку категории новостей
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
        await callback.message.answer("Не удалось получить новости. Попробуйте позже.")



 # обработчик нажатия кнопки "Мои задачи" (из главного меню) — пока заглушка
@dp.message(F.text == "Мои задачи")
async def tasks_button_handler(message: Message):
    await message.answer("Менеджер задач в разработке 🚧")



