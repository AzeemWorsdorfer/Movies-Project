import app.cli as cli
import storage.movie_storage_sql as movie_storage

# ---------------- Main Entry ---------------- #


def main():
    """
    Main entry point for the application.
    Initializes database and handles user switching loop.
    """
    # 1. Initialize the database schema
    movie_storage.initialize_database()

    cli.print_welcome()

    # Outer loop for user selection/switching
    app_running = True
    while app_running:
        user_id, user_name = cli.select_user()

        # Inner loop runs the menu for the active user
        session_running = True
        while session_running:
            # run_user_session returns True to switch users, or False to exit app
            switch_user_requested = cli.run_user_session(user_id, user_name)

            if switch_user_requested is False:
                app_running = False
                session_running = False
            elif switch_user_requested is True:
                session_running = False


if __name__ == "__main__":
    main()
