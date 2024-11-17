# config.py

from dotenv import load_dotenv
import os

# Загрузка переменных окружения из .env файла
load_dotenv()


class Config:
    TELEGRAM_API_TOKEN = os.getenv('TELEGRAM_API_TOKEN', 'BOT_TOKEN')
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY', 'WEATHER_API_KEY')
    EXCHANGE_API_KEY = os.getenv('EXCHANGE_API_KEY', 'EXCHANGE_API_KEY')
    X_RAPID_API_KEY = os.getenv('X_RAPID_API_KEY', 'X_RAPID_API_KEY')
