# utils/currency.py

import requests


def get_exchange_rate(api_key: str, base_currency: str, target_currency: str) -> str:
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/pair/{base_currency}/{target_currency}"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 200 and data["result"] == "success":
        rate = data["conversion_rate"]
        return f"Курс {base_currency} к {target_currency}: {rate}"
    else:
        return "Не удалось получить курс валют."


def get_all_currencies(api_key):
    url = f"https://openexchangerates.org/api/currencies.json?app_id={api_key}"
    response = requests.get(url)
    data = response.json()
    return "\n".join([f"{code}: {name}" for code, name in data.items()])
