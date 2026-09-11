import os
import requests
import streamlit as st
from dotenv import load_dotenv


# ---------------- LOAD ENVIRONMENT ---------------- #

load_dotenv()


# ---------------- TMDB API KEY ---------------- #

API_KEY = os.getenv("TMDB_API_KEY")

# If running on Streamlit Cloud, get key from Secrets
if not API_KEY:
    API_KEY = st.secrets.get("TMDB_API_KEY")


# ---------------- TMDB SETTINGS ---------------- #

BASE_URL = "https://api.themoviedb.org/3"

IMAGE_BASE_URL = "https://image.tmdb.org/t/p/w500"


# ---------------- GET MOVIE DETAILS ---------------- #

def get_movie_details(tmdb_id):

    if tmdb_id is None:
        return None

    if not API_KEY:
        return None

    try:

        url = f"{BASE_URL}/movie/{int(tmdb_id)}"

        params = {
            "api_key": API_KEY
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        if response.status_code == 200:
            return response.json()

        return None

    except Exception:
        return None


# ---------------- GET POSTER URL ---------------- #

def get_poster_url(poster_path):

    if poster_path:

        return IMAGE_BASE_URL + poster_path

    return None