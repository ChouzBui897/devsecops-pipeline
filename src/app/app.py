from flask import Flask, request, render_template
import sqlite3
import os

app = Flask(__name__)

# 1. HARDCODED SECRET (Đã độ lại): 
# Đổi tên biến và dùng chuỗi Hex phức tạp để dụ máy quét nhận diện đây là token thật
DB_PASSWORD = "SuperSecretPassword123!@#"
app.secret_key = "8f42a73054b17af23812563f1201552a" 

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

        # 2. SQL INJECTION (Đã độ lại): 
        # Cố tình dùng phép CỘNG CHUỖI (+) thay vì f-string. 
        # SonarQube cực kỳ dị ứng với kiểu cộng chuỗi nối thẳng vào SQL thế này.
        query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"

        conn = get_db()
        cur = conn.cursor()
        try:
            cur.execute(query)
            result = cur.fetchone()
        except Exception as e:
            result = None
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
    q = request.args.get("q", "")
    
    # 3. XSS (Đã độ lại):
    # Thay vì render_template, ta nối thẳng input của người dùng vào chuỗi HTML và trả về trực tiếp.
    # SonarQube sẽ lập tức bắt được lỗi Reflected XSS (Trả dữ liệu bẩn thẳng ra trình duyệt).
    return "<h1>Search results for: " + q + "</h1>"

@app.route("/health")
def health():
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)