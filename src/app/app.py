from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

# Hardcoded secret (intentional vulnerability - for SAST)
app.secret_key = "hardcoded_secret_key"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "database.db")

def get_db():
    return sqlite3.connect(DB_NAME)

@app.route("/")
def index():
    return render_template("index.html", title="Home")

@app.route("/login", methods=["GET", "POST"])
def login():
    message = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # SQL Injection vulnerability (intentional - for DAST)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(query)
            result = cur.fetchone()
        except Exception as e:
            result = None
            message = f"DB error: {e}"
        finally:
            conn.close()

        message = f"Welcome {username}" if result else (message or "Login failed")

    return render_template("login.html", title="Login", message=message)

@app.route("/search")
def search():
    q = request.args.get("q")
    # XSS vulnerability is intentionally in template via {{ q | safe }}
    return render_template("search.html", title="Search", q=q)

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
