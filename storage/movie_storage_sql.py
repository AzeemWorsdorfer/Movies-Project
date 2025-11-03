from sqlalchemy import create_engine, text

# Define database URL
DATABASE_URL = "sqlite:///data/movies.db"

# Create a database engine
engine = create_engine(DATABASE_URL, echo=True)


def initialize_database():
    """Ensures the users and movies tables are created upon startup."""
    with engine.connect() as connection:
        # Create the users table
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL
            )
        """))

        # Create the movies table
        connection.execute(text("""
            CREATE TABLE IF NOT EXISTS movies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                year INTEGER NOT NULL,
                rating REAL NOT NULL,
                poster_url TEXT,
                user_id INTEGER NOT NULL,  
                FOREIGN KEY (user_id) REFERENCES users(id),
                UNIQUE(title, user_id) 
            )
        """))
        connection.commit()


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


def add_movie(title, year, rating, poster_url, user_id):
    """Add a new movie to the database."""
    with engine.connect() as connection:
        try:
            connection.execute(text("INSERT INTO movies (title, year, rating, poster_url, user_id) VALUES (:title, :year, :rating, :poster_url, :user_id)"),
                               {"title": title,
                                "year": year,
                                "rating": rating,
                                "poster_url": poster_url,
                                "user_id": user_id
                                }
                               )
            connection.commit()
        except Exception as e:
            print(f"Error: {e}")


def delete_movie(title, user_id):
    """Delete a movie from the database."""
    with engine.connect() as connection:
        result = connection.execute(
            text("DELETE FROM movies WHERE title = :title AND user_id = :user_id"), {"title": title, "user_id": user_id})
        connection.commit()
        return result.rowcount > 0


def update_movie(title, rating, user_id):
    """Update the rating of a movie in the database."""
    with engine.connect() as connection:
        result = connection.execute(text("UPDATE movies SET rating = :rating WHERE title = :title AND user_id = :user_id"),
                                    {"title": title, "rating": rating, "user_id": user_id})
        connection.commit()
        return result.rowcount > 0
