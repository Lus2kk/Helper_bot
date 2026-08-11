from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

# главное меню кнопок
main_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Погода"), KeyboardButton(text="Новости")],
        [KeyboardButton(text="Мои задачи"), KeyboardButton(text="Помощь")],
    ],
    resize_keyboard=True,
)

# телеграмм-кнопка для запроса геолокации пользователя
location_keyboard = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Поделиться геолокацией", request_location=True)]],
    resize_keyboard=True,
)

# виды доступных топиков новостей
NEWS_TOPICS = {
    "sports": "Спорт",
    "technology": "Технологии",
    "entertainment": "Кино",
    "business": "Бизнес",
    "science": "Наука",
    "world": "Мир",
    "health": "Здоровье",
}

# кнопки категорий новостей, идут по 2 в ряд
def news_keyboard():
    builder = InlineKeyboardBuilder()
    for topic_key, topic_label in NEWS_TOPICS.items():
        builder.button(text=topic_label, callback_data=f"news:{topic_key}")
    builder.adjust(2)
    return builder.as_markup()