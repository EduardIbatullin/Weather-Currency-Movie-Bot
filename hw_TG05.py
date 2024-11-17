# bot.py

from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.memory import MemoryStorage
from config import Config
from utils.weather import get_weather
from utils.currency import get_exchange_rate, get_all_currencies
from utils.movies import get_random_movies
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

# Инициализация бота, диспетчера и FSM-хранилища
bot = Bot(token=Config.TELEGRAM_API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Определение состояний для FSM
class WeatherState(StatesGroup):
    city = State()

class CurrencyState(StatesGroup):
    from_currency = State()
    to_currency = State()

# Главный обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: Message):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Погода")],
            [types.KeyboardButton(text="Курс валют")],
            [types.KeyboardButton(text="Топ фильмов")]
        ],
        resize_keyboard=True
    )
    await message.answer("Привет! Выберите действие:", reply_markup=keyboard)

# Обработчик выбора "Погода"
@dp.message(lambda message: message.text == "Погода")
async def weather_start(message: Message, state: FSMContext):
    await message.answer("Введите город:")
    await state.set_state(WeatherState.city)

@dp.message(WeatherState.city)
async def get_city_weather(message: Message, state: FSMContext):
    city = message.text
    weather_data = get_weather(Config.WEATHER_API_KEY, city)
    await message.answer(weather_data)
    await state.clear()

# Обработчик выбора "Курс валют"
@dp.message(lambda message: message.text == "Курс валют")
async def currency_start(message: Message, state: FSMContext):
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=[
            [types.KeyboardButton(text="Показать все валюты")],
        ],
        resize_keyboard=True
    )
    await message.answer("Введите код первой валюты (например, USD):", reply_markup=keyboard)
    await state.set_state(CurrencyState.from_currency)

@dp.message(lambda message: message.text == "Показать все валюты")
async def show_all_currencies(message: Message):
    currencies = get_all_currencies(Config.EXCHANGE_API_KEY)
    await message.answer(currencies)

@dp.message(CurrencyState.from_currency)
async def get_from_currency(message: Message, state: FSMContext):
    from_currency = message.text.upper()
    await state.update_data(from_currency=from_currency)
    await message.answer("Введите код второй валюты (например, RUB):")
    await state.set_state(CurrencyState.to_currency)

@dp.message(CurrencyState.to_currency)
async def get_to_currency(message: Message, state: FSMContext):
    data = await state.get_data()
    from_currency = data['from_currency']
    to_currency = message.text.upper()
    exchange_data = get_exchange_rate(Config.EXCHANGE_API_KEY, from_currency, to_currency)
    await message.answer(exchange_data)
    await state.clear()

# Обработчик выбора "Топ фильмов"
@dp.message(lambda message: message.text == "Топ фильмов")
async def top_movies_start(message: Message):
    api_key = Config.X_RAPID_API_KEY
    movies_data = get_random_movies(api_key)

    if movies_data:
        for movie in movies_data:
            # Создаем инлайн-кнопку
            movie_link = InlineKeyboardButton(text="Подробнее на IMDb", url=movie['imdb_link'])
            inline_kb = InlineKeyboardMarkup(inline_keyboard=[[movie_link]])

            # Отправляем сообщение с картинкой, описанием и кнопкой
            if movie['image']:
                await message.answer_photo(
                    photo=movie['image'],
                    caption=f"{movie['title']} ({movie['year']})\n{', '.join(movie['genre'])}\nРейтинг: {movie['rating']}\n{movie['description']}",
                    reply_markup=inline_kb
                )
            else:
                await message.answer(
                    text=f"{movie['title']} ({movie['year']})\n{', '.join(movie['genre'])}\nРейтинг: {movie['rating']}\n{movie['description']}",
                    reply_markup=inline_kb
                )
    else:
        await message.answer("Ошибка при получении данных о фильмах.")

# Запуск бота
if __name__ == "__main__":
    dp.run_polling(bot)
