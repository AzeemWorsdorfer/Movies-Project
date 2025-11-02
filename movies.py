import random
import statistics
import movie_storage_sql as movie_storage
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
    print("********** My Movies Database **********\n")


def print_menu():
    """
    Displays the menu options for the user.
    """
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

# ---------------- Core Functionality ---------------- #


def list_movies():
    """
    Lists all movies from database with their year and rating.
    """
    movies = movie_storage.get_movies()

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


def add_movie():
    """
    Adds a new movie to the database using data fetched from OMDb API.
    Handles connection errors and 'movie not found' errors.
    """
    title = safe_title_input("Enter movie name: ")

    movies = movie_storage.get_movies()

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
        poster_url=movies_data["poster_url"]
    )

    print(f"Movie {title} successfully added")


def delete_movie():
    """
    Deletes a movie from the database.
    """
    title = safe_title_input("Enter movie name to delete: ")

    if movie_storage.delete_movie(title):
        print(f"Movie {title} successfully deleted")
    else:
        # This catches the case where the movie was not in the DB
        print(f"Movie {title} doesn't exist")


def update_movie():
    """
    Updates the rating of a movie in the database.
    """
    movies = movie_storage.get_movies()

    title = safe_title_input("Enter movie name: ")
    if title not in movies:
        print(f"Movie {title} doesn't exist")
        return

    rating = safe_float_input("Enter new movie rating (1–10): ")

    movie_storage.update_movie(title, rating)
    print(f"Movie {title} successfully updated")


def stats():
    """
    Displays statistics about all movies in the database:
    - Average rating
    - Median rating
    - Best movie(s)
    - Worst movie(s)
    """
    movies = movie_storage.get_movies()
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


def random_movie():
    """
    Picks and displays a random movie from the database.
    """
    movies = movie_storage.get_movies()

    if not movies:
        print("No movies in the database.")
        return

    title = random.choice(list(movies.keys()))
    data = movies[title]
    rating = data["rating"]
    year = data["year"]

    print(f"Your movie for tonight: {title} ({year}), rated {rating}")


def search_movie():
    """
    Searches for movies containing a user-provided string in the title
    and displays them with year and rating.
    """
    movies = movie_storage.get_movies()

    query = safe_title_input("Enter part of the movie name: ").lower()
    found = False

    for title, data in movies.items():
        if query in title.lower():
            print(f"{title} ({data['year']}): {data['rating']}")
            found = True

    if not found:
        print("No matching movies found.")


def movies_sorted_by_rating():
    """
    Lists all movies sorted by rating (highest to lowest).
    Handles empty database gracefully.
    """
    movies = movie_storage.get_movies()

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


def movies_sorted_by_year():
    """
    Lists all movies sorted by year (chronological order).
    Asks the user whether to display latest movies first or last
    """
    movies = movie_storage.get_movies()

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


def generate_website():
    """
    Generates a full HTML website from the movie database using a template.
    """
    TEMPLATE_PATH = "index_template.html"
    OUTPUT_PATH = "index.html"
    APP_TITLE = "My Movie App"  # <--- Choose your title here!

    # 2. Get all movie data
    movies = movie_storage.get_movies()
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

def run_menu():
    """
    Runs the main program loop, handling user input and actions.
    Includes a global try/except to prevent crashes.
    """
    while True:
        try:
            print_menu()
            print()
            choice = input("Enter choice (0–10): ").strip()
            print()

            if choice == "0":
                print("Bye 👋 Thanks for using My Movies Database!")
                break
            elif choice == "1":
                list_movies()
            elif choice == "2":
                add_movie()
            elif choice == "3":
                delete_movie()
            elif choice == "4":
                update_movie()
            elif choice == "5":
                stats()
            elif choice == "6":
                random_movie()
            elif choice == "7":
                search_movie()
            elif choice == "8":
                movies_sorted_by_rating()
            elif choice == "9":
                movies_sorted_by_year()
            elif choice == "10":
                generate_website()
            else:
                print("Invalid choice. Please enter a number from 0–10.")

            print()
            wait_for_enter()
            print()

        except Exception as e:
            print(f"\n⚠️ Oops! Something went wrong: {e}")
            print("Don’t worry, you can try again.\n")


# ---------------- Main Entry ---------------- #

def main():
    """
    Main function to start the program.
    """
    print_welcome()
    run_menu()


if __name__ == "__main__":
    main()
