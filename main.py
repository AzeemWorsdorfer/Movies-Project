import random
import statistics
import storage.movie_storage_sql as movie_storage
import movies_api as api
import requests

# ---------------- Helper Functions ---------------- #


def create_movie_tiles(movies):
    """
    Generates the HTML grid content for all movies.

    Args:
        movies (dict): The dictionary of movies from movie_storage.get_movies()

    Returns:
        str: The HTML string for the movie grid.
    """
    html_content = ""

    for title, data in movies.items():
        movie_title = title.replace('"', "'")
        movie_year = data['year']
        poster_url = data['poster_url']

        rating = data['rating']

        # Build the HTML list item:
        movie_html = f"""
        <li>
            <div class="movie">
                <img class="movie-poster"
                     src="{poster_url}"
                     alt="{movie_title} - Rating: {rating}">
                <div class="movie-title">{movie_title}</div>
                <div class="movie-year">({movie_year})</div>
            </div>
        </li>
        """

        html_content += movie_html

    return html_content


def safe_title_input(prompt):
    """
    Asks for a non-empty movie title until valid input is given.
    """
    while True:
        title = input(prompt).strip()
        if title:
            
            return title
        print("Movie title cannot be empty. Please try again.")


def safe_float_input(prompt):
    """
    Asks for a float input safely, keeps asking until valid input is given.
    """
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


def safe_int_input(prompt):
    """
    Asks for an integer input safely, keeps asking until valid input is given.
    """
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Invalid input. Please enter an integer.")


def wait_for_enter():
    """
    Waits until the user presses only Enter to continue.
    """
    while True:
        key = input("Press Enter to continue...")
        if key == "":
            break


# ---------------- UI / Display Functions ---------------- #

def print_welcome():
    """
    Prints the welcome message for the program.
    """
    print("********** My Movies App **********\n")


# ---------------- Core Functionality ---------------- #


def list_movies(user_id):
    """
    Lists all movies from database with their year and rating.
    """
    movies = movie_storage.get_movies(user_id)

    if not movies:
        print("No movies in the database.")
        return

    print(f"{len(movies)} movies in total")
    print("-" * 30)

    for title, data in movies.items():
        print(f"🎬 {title} ({data['year']}): {data['rating']}")
        # Display the poster URL so the user knows it was fetched
        if data.get('poster_url') and data['poster_url'] != 'N/A':
            print(f"   Poster: {data['poster_url']}")
        print("-" * 30)


def add_movie(user_id):
    """
    Adds a new movie to the database using data fetched from OMDb API.
    Handles connection errors and 'movie not found' errors.
    """
    title = safe_title_input("Enter movie name: ")

    movies = movie_storage.get_movies(user_id)

    if title in movies:
        print(f"Movie {title} already exists!")
        return

    try:
        print(f"Searching OMDb for '{title}'...")
        movies_data = api.get_movie_data(title)
    except requests.exceptions.RequestException:
        print(
            "Error: Could not connect to OMDb API. Please check your internet connection.")
        return

    if movies_data is None:
        print(
            f"❌ Movie '{title}' not found in OMDb. Please try another title.")
        return

    movie_storage.add_movie(
        title=movies_data["title"],
        year=movies_data["year"],
        rating=movies_data["rating"],
        poster_url=movies_data["poster_url"],
        user_id=user_id
    )

    print(f"Movie {title} successfully added")


def delete_movie(user_id):
    """
    Deletes a movie from the database.
    """
    title = safe_title_input("Enter movie name to delete: ")

    if movie_storage.delete_movie(title, user_id):
        print(f"Movie {title} successfully deleted")
    else:
        # This catches the case where the movie was not in the DB
        print(f"Movie {title} doesn't exist")


def update_movie(user_id):
    """
    Updates the rating of a movie in the database.
    """
    movies = movie_storage.get_movies(user_id)

    title = safe_title_input("Enter movie name: ")
    if title not in movies:
        print(f"Movie {title} doesn't exist")
        return

    rating = safe_float_input("Enter new movie rating (1–10): ")

    movie_storage.update_movie(title, rating, user_id)
    print(f"Movie {title} successfully updated")


def stats(user_id):
    """
    Displays statistics about all movies in the database:
    - Average rating
    - Median rating
    - Best movie(s)
    - Worst movie(s)
    """
    movies = movie_storage.get_movies(user_id)
    if not movies:
        print("No movies in the database.")
        return

    ratings = [data["rating"] for data in movies.values()]
    average = statistics.mean(ratings)
    median = statistics.median(ratings)

    max_rating = max(ratings)
    best_movies = [title for title,
                   data in movies.items() if data['rating'] == max_rating]

    min_rating = min(ratings)
    worst_movies = [title for title,
                    data in movies.items() if data['rating'] == min_rating]

    print(f"Average rating: {average:.1f}")
    print(f"Median rating: {median:.1f}")
    print(f"Best movie(s) ({max_rating}): {', '.join(best_movies)}")
    print(f"Worst movie(s) ({min_rating}): {', '.join(worst_movies)}")


def random_movie(user_id):
    """
    Picks and displays a random movie from the database.
    """
    movies = movie_storage.get_movies(user_id)

    if not movies:
        print("No movies in the database.")
        return

    title = random.choice(list(movies.keys()))
    data = movies[title]
    rating = data["rating"]
    year = data["year"]

    print(f"Your movie for tonight: {title} ({year}), rated {rating}")


def search_movie(user_id):
    """
    Searches for movies containing a user-provided string in the title
    and displays them with year and rating.
    """
    movies = movie_storage.get_movies(user_id)

    query = safe_title_input("Enter part of the movie name: ").lower()
    found = False

    for title, data in movies.items():
        if query in title.lower():
            print(f"{title} ({data['year']}): {data['rating']}")
            found = True

    if not found:
        print("No matching movies found.")


def movies_sorted_by_rating(user_id):
    """
    Lists all movies sorted by rating (highest to lowest).
    Handles empty database gracefully.
    """
    movies = movie_storage.get_movies(user_id)

    if not movies:
        print("No movies in the database to sort.")
        return

    sorted_movies = sorted(
        movies.items(),
        key=lambda item: item[1]["rating"],
        reverse=True
    )

    print("Movies sorted by rating (highest → lowest):")
    for title, data in sorted_movies:
        print(f"{title} ({data['year']}): {data['rating']}")


def movies_sorted_by_year(user_id):
    """
    Lists all movies sorted by year (chronological order).
    Asks the user whether to display latest movies first or last
    """
    movies = movie_storage.get_movies(user_id)

    if not movies:
        print("No movies in the database to sort.")
        return

    while True:
        choice = input("Show latest movies first? (y/n): ").strip().lower()
        if choice in ('y', 'n'):
            reverse_order = True if choice == 'y' else False
            break
        print("Invalid input. Please enter 'y' for yes or 'n' for no.")

    sorted_movies = sorted(
        movies.items(),
        key=lambda item: item[1]["year"],
        reverse=reverse_order
    )

    print("Movies sorted by year:")
    for title, data in sorted_movies:
        print(f"{title} ({data['year']}): {data['rating']}")


def generate_website(user_id, user_name):
    """
    Generates a full HTML website from the movie database using a template.
    """
    TEMPLATE_PATH = "_static/index_template.html"
    OUTPUT_PATH = f"{user_name.replace(' ', '_')}.html"
    APP_TITLE = f"{user_name}'s Movie App"

    # 2. Get all movie data
    movies = movie_storage.get_movies(user_id)
    if not movies:
        print("Cannot generate website: The database is empty.")
        return

    # 3. Generate the movie grid HTML
    movie_grid_html = create_movie_tiles(movies)

    # 4. Read the template file
    try:
        with open(TEMPLATE_PATH, 'r') as f:
            template_content = f.read()
    except FileNotFoundError:
        print(
            f"Error: HTML template file not found at {TEMPLATE_PATH}. Check your _static folder.")
        return

    # 5. Replace the placeholders
    final_html = template_content.replace("__TEMPLATE_TITLE__", APP_TITLE)
    final_html = final_html.replace("__TEMPLATE_MOVIE_GRID__", movie_grid_html)

    # 6. Write the final HTML file
    try:
        with open(OUTPUT_PATH, 'w') as f:
            f.write(final_html)

        # 7. Print success message
        print("✅ Website was generated successfully.")
    except Exception as e:
        print(f"❌ Error writing the output file {OUTPUT_PATH}: {e}")


# ---------------- Program Loop ---------------- #
# In main.py, add these functions above run_menu:

def get_all_users():
    """Retrieves all users from the database for display."""
    # Use a direct query since this logic isn't in movie_storage yet
    import sqlite3
    try:
        conn = sqlite3.connect('data/movies.db')
        cursor = conn.cursor()
        cursor.execute("SELECT id, name FROM users")
        users = cursor.fetchall()
        conn.close()
        return users
    except sqlite3.OperationalError:
        # Happens if the database file is new and the table hasn't been created yet.
        return []


def select_user():
    """
    Displays existing users, allows creation of a new user, and returns the selected user's ID and name.
    """
    while True:
        users = get_all_users()
        print("\nWelcome to the Movie App! 🎬")
        print("Select a user:")

        user_map = {}
        for i, (user_id, name) in enumerate(users, 1):
            print(f"{i}. {name}")
            user_map[str(i)] = (user_id, name)

        create_option = len(users) + 1
        print(f"{create_option}. Create new user")

        choice = input("Enter choice: ").strip()

        if choice in user_map:
            user_id, name = user_map[choice]
            print(f"\nWelcome back, {name}! 🎬")
            return user_id, name

        elif choice == str(create_option):
            new_name = safe_title_input("Enter new username: ")

            # Use the storage function to create the new user
            new_id = movie_storage.create_new_user(new_name)

            if new_id:
                print(f"✅ User '{new_name}' created!")
                return new_id, new_name
            else:
                print(
                    f"User '{new_name}' already exists. Please choose another name.")

        else:
            print("Invalid choice. Please try again.")


def print_menu_with_user(user_name):
    """
    Displays the menu options for the user, showing the active user's name.
    """
    print(f"\n--- Active User: {user_name} ---")
    print("Menu:")
    print("0. Exit")
    print("1. List movies")
    print("2. Add movie")
    print("3. Delete movie")
    print("4. Update movie")
    print("5. Stats")
    print("6. Random movie")
    print("7. Search movie")
    print("8. Movies sorted by rating")
    print("9. Movies sorted by year")
    print("10. Generate Website")
    print("11. Switch User")


def run_user_session(user_id, user_name):
    """
    Runs the main program loop for an active, logged-in user.
    """
    while True:
        try:
            print_menu_with_user(user_name)
            print()
            choice = input("Enter choice (0–11): ").strip()
            print()

            if choice == "0":
                print(f"Bye, {user_name}! 👋")
                return False
            elif choice == "11":
                print(f"Switching user from {user_name}...")
                return True
            elif choice == "1":
                list_movies(user_id)
            elif choice == "2":
                add_movie(user_id)
            elif choice == "3":
                delete_movie(user_id)
            elif choice == "4":
                update_movie(user_id)
            elif choice == "5":
                stats(user_id)
            elif choice == "6":
                random_movie(user_id)
            elif choice == "7":
                search_movie(user_id)
            elif choice == "8":
                movies_sorted_by_rating(user_id)
            elif choice == "9":
                movies_sorted_by_year(user_id)
            elif choice == "10":
                generate_website(user_id, user_name)
            else:
                print("Invalid choice. Please enter a number from 0–11.")

            print()
            wait_for_enter()
            print()

        except Exception as e:
            print(f"\n⚠️ Oops! Something went wrong: {e}")
            print("Don’t worry, you can try again.\n")


# ---------------- Main Entry ---------------- #

def main():
    """
    Main function to start the program and handle user switching.
    """
    movie_storage.initialize_database()
    
    print_welcome()
    app_running = True
    while app_running:
        user_id, user_name = select_user()

        
        session_running = True
        while session_running:
            
            switch_user_requested = run_user_session(user_id, user_name)

            if switch_user_requested is False:
                app_running = False
                session_running = False
            elif switch_user_requested is True:
                session_running = False


if __name__ == "__main__":
    main()
