from sqlalchemy import create_engine, text

# Define database URL
DATABASE_URL = "sqlite:///data/movies.db"

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
            poster_url TEXT,
            user_id INTERGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            UNIQUE(title, user_id)
        )
    """))
    connection.commit()

    print("WARNING: Clearing old records to match updated table structure...")
    connection.execute(text("DELETE FROM movies"))
    connection.commit()
    print("Database structure updated and old records cleared.")


def get_user_by_name(name):
    """Retrieves a user's ID and name from the database, or None if not found."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT id, name FROM users WHERE name = :name"),
            {"name": name}
        ).fetchone()

        if result:
            # Return as a dictionary for easy access (e.g., user['id'])
            return {"id": result[0], "name": result[1]}
        return None


def create_new_user(name):
    """Adds a new user to the database and returns their newly created ID."""
    with engine.connect() as connection:
        # Check if user already exists
        if get_user_by_name(name):
            return None

        result = connection.execute(
            text("INSERT INTO users (name) VALUES (:name) RETURNING id"),
            {"name": name}
        )

        new_id = result.fetchone()[0]
        connection.commit()
        return new_id


def get_movies(user_id):
    """Retrieves all movies from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT title, year, rating, poster_url FROM movies WHERE user_id = :user_id"), {
                "user_id": user_id}
        )
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
