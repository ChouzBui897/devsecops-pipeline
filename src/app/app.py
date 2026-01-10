from flask import Flask, request
import sqlite3

app = Flask(__name__)

# Hardcoded secret (intentional vulnerability)
SECRET_KEY = "hardcoded_secret_key"

def get_db():
    conn = sqlite3.connect("database.db")
    return conn

@app.route("/")
def index():
    return """
        <h2>DevSecOps Demo App</h2>
        <a href='/login'>Login</a><br>
        <a href='/search'>Search</a>
    """

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # SQL Injection vulnerability (intentional)
        query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(query)
        result = cursor.fetchone()

        if result:
            return f"Welcome {username}"
        else:
            return "Login failed"

    return """
        <h3>Login</h3>
        <form method="post">
            Username: <input name="username"><br>
            Password: <input name="password"><br>
            <input type="submit">
        </form>
    """

@app.route("/search")
def search():
    keyword = request.args.get("q", "")
    # XSS vulnerability (intentional)
    return f"<h3>Search result for: {keyword}</h3>"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
