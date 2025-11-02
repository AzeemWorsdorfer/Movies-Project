import random
import statistics
import movie_storage_sql as movie_storage


# ---------------- Helper Functions ---------------- #

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
    for title, data in movies.items():
        print(f"{title} ({data['year']}): {data['rating']}")


def add_movie():
    """
    Adds a new movie to the database.
    """
    movies = movie_storage.get_movies()

    title = safe_title_input("Enter movie name: ")
    if title in movies:
        print(f"Movie {title} already exists!")
        return

    rating = safe_float_input("Enter rating (1–10): ")
    year = safe_int_input("Enter the year: ")

    movie_storage.add_movie(title, year, rating)
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
            choice = input("Enter choice (0–9): ").strip()
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
            else:
                print("Invalid choice. Please enter a number from 0–9.")

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
