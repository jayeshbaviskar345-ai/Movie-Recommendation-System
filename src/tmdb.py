import os
import requests
from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("TMDB_API_KEY")


BASE_URL = "https://api.themoviedb.org/3"


IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


def get_movie_details(tmdb_id):

    if tmdb_id is None:
        return None

    url = f"{BASE_URL}/movie/{int(tmdb_id)}"

    params = {
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        return response.json()

    return None



def get_poster_url(poster_path):

    if poster_path:
        return IMAGE_BASE_URL + poster_path

    return None


