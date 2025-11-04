import app.core as core
import storage.movie_storage_sql as movie_storage
import sqlite3

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
    print("********** My Movies App **********\n")


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
    print("12. Delete User")


def run_user_session(user_id, user_name):
    """
    Runs the main program loop for an active, logged-in user.
    """
    while True:
        try:
            print_menu_with_user(user_name)
            print()
            choice = input("Enter choice (0–12): ").strip()
            print()

            if choice == "0":
                print(f"Bye, {user_name}! 👋")
                return False
            elif choice == "1":
                core.list_movies(user_id)
            elif choice == "2":
                core.add_movie(user_id)
            elif choice == "3":
                core.delete_movie(user_id)
            elif choice == "4":
                core.update_movie(user_id)
            elif choice == "5":
                core.stats(user_id)
            elif choice == "6":
                core.random_movie(user_id)
            elif choice == "7":
                core.search_movie(user_id)
            elif choice == "8":
                core.movies_sorted_by_rating(user_id)
            elif choice == "9":
                core.movies_sorted_by_year(user_id)
            elif choice == "10":
                core.generate_website(user_id, user_name)
            elif choice == "11":
                print(f"Switching user from {user_name}...")
                return True
            elif choice == "12":
                return delete_active_user(user_id, user_name)
            else:
                print("Invalid choice. Please enter a number from 0–12.")

            print()
            wait_for_enter()
            print()

        except Exception as e:
            print(f"\n⚠️ Oops! Something went wrong: {e}")
            print("Don’t worry, you can try again.\n")


def delete_active_user(user_id, user_name):
    """Handles the process of deleting the currently logged-in user."""
    print(f"\n⚠️ WARNING: You are about to delete user '{user_name}' and ALL their movies.")
    confirmation = input("Type 'DELETE' to confirm this action: ").strip()

    if confirmation == "DELETE":
        # 1. Delete dependent rows (movies)
        movies_deleted = movie_storage.delete_movies_by_user_id(user_id)
        
        # 2. Delete the user
        user_deleted = movie_storage.delete_user(user_id)
        
        if user_deleted:
            print(f"✅ User '{user_name}' and {movies_deleted} movie(s) successfully deleted.")
            # Returns True to force user switch/exit after successful deletion
            return True 
        else:
            print(f"❌ Error: Could not delete user '{user_name}'.")
            return False
    else:
        print("User deletion cancelled.")
        return False