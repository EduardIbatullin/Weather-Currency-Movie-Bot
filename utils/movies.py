import requests
import random
from deep_translator import GoogleTranslator


def get_random_movies(api_key):
    try:
        url = "https://imdb-top-100-movies.p.rapidapi.com/"
        headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "imdb-top-100-movies.p.rapidapi.com"
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        movies = response.json()

        if not isinstance(movies, list) or len(movies) == 0:
            raise ValueError("Некорректный формат ответа от API")

        random_movies = random.sample(movies, 5)

        # Переводим данные на русский язык
        translator = GoogleTranslator(source='auto', target='ru')
        for movie in random_movies:
            movie['title'] = translator.translate(movie['title'])
            movie['description'] = translator.translate(movie['description'])
            movie['genre'] = [translator.translate(genre) for genre in movie['genre']]

        return random_movies

    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе к API: {e}")
    except ValueError as e:
        print(f"Ошибка при обработке данных: {e}")
    except Exception as e:
        print(f"Произошла непредвиденная ошибка: {e}")

    return None
