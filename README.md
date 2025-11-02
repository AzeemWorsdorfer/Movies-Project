# My Movie Database App 🎬

A simple **Python command-line application** for managing a personal movie collection. It uses the **OMDb API** to automatically fetch movie details and stores everything in a **SQLite** database.

---

## ✨ Key Features

* **Quick Add:** Automatically fetches movie title, year, rating, and poster URL from OMDb when you add a movie.
* **Database:** Stores data locally using SQLAlchemy and SQLite (in the `/data` folder).
* **Stats:** Calculates average rating, median rating, and identifies best/worst movies.
* **Web View:** Generates a basic static HTML website (`index.html`) to display your collection.

---

## ⚙️ Setup

### Prerequisites

* Python 3.6+
* An API Key from [OMDb API](http://www.omdbapi.com/apikey.aspx)

### Installation Steps

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

---

## 🚀 How to Run

1.  **Start the application:**
    ```bash
    python main.py
    ```

2.  **Use the Menu:** Follow the on-screen menu.
    * Use **`2` (Add movie)** to search OMDb and save new movies.
    * Use **`10` (Generate Website)** to create the `index.html` file in the root directory.

---
