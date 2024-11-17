import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
import random
import requests

from config import Config


#  Инициализация бота и диспетчера
bot = Bot(token=Config.TELEGRAM_API_TOKEN)
dp = Dispatcher()


def get_cats_breeds():
    url = "https://api.thecatapi.com/v1/breeds"
    headers = {"x-api-key": Config.THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()


def get_cat_image_by_breed(breed_id):
    url = f"https://api.thecatapi.com/v1/images/search?breed_ids={breed_id}"
    headers = {"x-api-key": Config.THE_CAT_API_KEY}
    response = requests.get(url, headers=headers)
    return response.json()[0]["url"]


def get_breed_info(breed_name):
    breeds = get_cats_breeds()
    for breed in breeds:
        if breed["name"].lower() == breed_name.lower():
            return breed
    return None


@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(f"Привет, {message.from_user.full_name}!")
    await message.answer("Напиши мне название породы кота и я выведу его фото и информацию о ней.")


@dp.message()
async def send_cat_info(message: Message):
    breed_name = message.text
    breed_info = get_breed_info(breed_name)
    if breed_info:
        cat_image_url = get_cat_image_by_breed(breed_info["id"])
        info = (f"Порода: {breed_info['name']} \n"
                f"Описание: {breed_info['description']} \n"
                f"Продолжительность жизни: {breed_info['life_span']} лет\n")
        await message.answer_photo(cat_image_url, caption=info)
    else:
        await message.answer("Такой породы кота нет. Попробуйте еще раз.")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())