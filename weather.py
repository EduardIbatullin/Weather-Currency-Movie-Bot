# utils/weather.py

import requests


def get_weather(api_key: str, city: str) -> str:
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&lang=ru"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather = data['current']['condition']['text']
        temp = data['current']['temp_c']
        return f"Погода в {city}: {weather}, температура: {temp}°C"
    else:
        return "Не удалось получить погоду."
