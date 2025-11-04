# 🎬 My Movies App

Welcome to **My Movies App**, a command-line application designed to help users manage, rate, and track their personal movie collections. The application now supports **multiple user profiles** with isolated movie databases and features a clean, modular architecture for easy maintenance and future expansion.

## ✨ Features

* **Multi-User Profiles:** Each user maintains a unique, personalized movie collection, ratings, and statistics.
* **User Management:** Easily create new profiles, switch between existing users (Option 11), or delete your profile and all associated data (Option 12).
* **OMDb Integration:** Add movies by name; the app automatically fetches the release year, professional rating, and poster URL.
* **CRUD Operations:** List, Add, Update, and Delete movies.
* **Movie Stats:** Get quick stats, including average rating, median rating, and lists of best/worst movies.
* **Sorting & Searching:** Sort movies by rating or year, and search titles using keywords.
* **Website Generation:** Generate a static HTML webpage showcasing the active user's movie collection and poster images.

## ⚙️ Architecture Overview

The application is structured into a modular package (`app/`) for maintainability and separation of concerns:

| File/Module | Responsibility | Details |
| :--- | :--- | :--- |
| `main.py` | **Entry Point** | Initializes the database schema and starts the main application loop. |
| `app/cli.py` | **UI / Flow Control** | Handles all user input (`input()`), output (`print()`), menu presentation, and manages the user session life cycle (select/switch/delete user). |
| `app/core.py` | **Business Logic** | Contains all core application logic: movie CRUD operations, statistics calculation, API interaction, and website generation. |
| `storage/` | **Data Persistence** | Manages all SQLAlchemy database interactions for `users`, `movies`, and schema setup. |

## 🚀 Setup and Installation

### Prerequisites

You need **Python 3.8+** installed on your system.

### Installation

1.  **Clone the Repository:**
    ```bash
    git clone [Your Repository URL Here]
    cd Movies-Project
    ```

2.  **Create a Virtual Environment** (Recommended):
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure your `requirements.txt` includes `requests` and `SQLAlchemy`)*

4.  **Set API Key:**
    The application uses the OMDb API. You need to create a free account and set your API key in the `.env` file located in the root directory:
    ```
    # .env
    OMDB_API_KEY=your_omdb_api_key_here
    ```

## ▶️ How to Run

Execute the main file to start the application:

```bash
python3 main.py