import requests
import os
from dotenv import load_dotenv

load_dotenv()

OMDB_API_KEY = os.environ.get("OMDB_API_KEY")

OMDB_URL = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&t="


def get_movie_data(title):
    """
      Fetches movie details (Title, Year, Rating, Poster) from OMDb API.

      Args:
          title (str): The title of the movie to search for.

      Returns:
          dict: A dictionary containing the required movie data, 
                OR None if the movie is not found.

      Raises:
          requests.exceptions.RequestException: If there's a connection error.
      """

    search_url = OMDB_URL + title

    try:
        response = requests.get(search_url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise e

    data = response.json()

    if data.get("Response") == "False":
        return None

    rating_str = data.get("imdbRating", "N/A")
    try:
        rating = float(rating_str) if rating_str != "N/A" else 0.0
    except ValueError:
        rating = 0.0

    movie_info = {
        "title": data.get("Title"),
        "year": int(data.get("Year")),
        "rating": rating,
        "poster_url": data.get("Poster")
    }
    return movie_info
