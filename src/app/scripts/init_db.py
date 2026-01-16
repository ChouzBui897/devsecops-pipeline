import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(os.path.dirname(BASE_DIR), "database.db")

def main():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()
    print("[OK] Database initialized:", DB_NAME)

if __name__ == "__main__":
    main()
