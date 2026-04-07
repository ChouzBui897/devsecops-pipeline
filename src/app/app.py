from flask import Flask, request, render_template
import sqlite3
import os
import hashlib
from markupsafe import escape

app = Flask(__name__)

# Vulnerability 1: Hardcoded Sensitive Data (CWE-798)
# Simulating a scenario where developers hardcode database credentials 
# or secret keys directly into the source code repository.
# DB_PASSWORD = "SuperSecretPassword123!@#"
# app.secret_key = "8f42a73054b17af23812563f1201552a" 
app.secret_key = os.environ.get('FLASK_SECRET_KEY', os.urandom(24))

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, "database.db")

def get_db():
    return sqlite3.connect(DB_NAME)

@app.after_request
def add_security_headers(response):
    # Chống Clickjacking (WARN 10020)
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    # Chống MIME-sniffing (WARN 10021)
    response.headers['X-Content-Type-Options'] = 'nosniff'
    # Cấu hình Content Security Policy cơ bản (WARN 10038)
    response.headers['Content-Security-Policy'] = "default-src 'self'"
    # Cấu hình Permissions Policy (WARN 10063)
    response.headers['Permissions-Policy'] = "geolocation=(), microphone=(), camera=()"
    return response

@app.route("/")
def index():
    return render_template("index.html", title="Home")

@app.route("/login", methods=["GET", "POST"])
def login():
    message = None

    if request.method == "POST":
        username = request.form.get("username", "")
        password = request.form.get("password", "")

        # Vulnerability 2: SQL Injection (CWE-89)
        # Improper Neutralization of Special Elements used in an SQL Command.
        # Directly concatenating user input into the SQL query string allows 
        # attackers to manipulate the statement logic (e.g., bypassing authentication).
        # query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
        query = "SELECT * FROM users WHERE username = ? AND password = ?"

        conn = get_db()
        cur = conn.cursor()
        try:
            # cur.execute(query)
            cur.execute(query, (username, password))
            result = cur.fetchone()
        except Exception as e:
            result = None
            # Information Exposure Through an Error Message (CWE-209)
            message = "DB error: " + str(e)
        finally:
            conn.close()

        if result:
            message = "Welcome " + username
        else:
            message = message or "Login failed"

    return render_template("login.html", title="Login", message=message)

@app.route("/search")
def search():
    # q = request.args.get("q", "")
    query = request.args.get("q", "")
    # Vulnerability 3: Reflected Cross-Site Scripting (XSS) (CWE-79)
    # The application receives input from an HTTP request and includes it in the 
    # immediate response in an unsafe way, without proper escaping.
    # return "<h1>Search results for: " + q + "</h1>"
    return f"<h1>Kết quả tìm kiếm cho: {escape(query)}</h1>"

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False) # nosec