import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(os.path.dirname(BASE_DIR), "database.db")

def main():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Insert demo users (simple approach for demo)
    cur.execute("INSERT INTO users(username, password) VALUES (?, ?)", ("admin", "admin123"))
    cur.execute("INSERT INTO users(username, password) VALUES (?, ?)", ("test", "test123"))

    conn.commit()
    conn.close()
    print("[OK] Seed data inserted.")

if __name__ == "__main__":
    main()
