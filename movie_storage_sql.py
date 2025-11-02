from sqlalchemy import create_engine, text

# Define database URL
DATABASE_URL = "sqlite:///movies.db"

# Create a database engine
engine = create_engine(DATABASE_URL, echo=True)

# Create the movies table if it does not exist
with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            poster_url TEXT
        )
    """))
    connection.commit()

    print("WARNING: Clearing old records to match updated table structure...")
    connection.execute(text("DELETE FROM movies"))
    connection.commit()
    print("Database structure updated and old records cleared.")


def get_movies():
    """Retrieves all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster_url FROM movies"))
        movies = result.fetchall()
    return {
        row[0]: {
            "year": row[1],
            "rating": row[2],
            "poster_url": row[3]
        }
        for row in movies
    }


def add_movie(title, year, rating, poster_url):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster_url) VALUES (:title, :year, :rating, :poster_url)"),
                               {"title": title,
                                "year": year,
                                "rating": rating,
                                "poster_url": poster_url
                                }
                               )
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title"), {"title": title})
        connection.commit()
        return result.rowcount > 0


def update_movie(title, rating):
    """Update the rating of a movie in the database."""
    with engine.connect() as connection:
        result = connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title"),
                                    {"title": title, "rating": rating})
        connection.commit()
        return result.rowcount > 0
