from flask import Flask, request, redirect, url_for, session, flash, send_from_directory, jsonify
import os

app = Flask(__name__)
app.secret_key = "change-this-to-a-secure-random-value"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Simple in-memory stores (replace with DB in production)
users = {}          # key: email -> {name, password}
submissions = []    # list of {title, content, author_email}

# Serve top-level static HTML files from repo root
@app.route("/")
def index():
    return send_from_directory(BASE_DIR, "index.html")

@app.route("/login.html")
def login_page():
    return send_from_directory(BASE_DIR, "login.html")

@app.route("/register.html")
def register_page():
    return send_from_directory(BASE_DIR, "register.html")

@app.route("/submit.html")
def submit_page():
    return send_from_directory(BASE_DIR, "submit.html")

@app.route("/admin.html")
def admin_page():
    return send_from_directory(BASE_DIR, "admin.html")

@app.route("/styles.css")
def styles():
    return send_from_directory(BASE_DIR, "styles.css")

# Form endpoints
@app.route("/register", methods=["POST"])
def register():
    email = request.form.get("email")
    name = request.form.get("name")
    password = request.form.get("password")
    if not email or not password:
        flash("Email and password required")
        return redirect(url_for("register_page"))
    if email in users:
        flash("User already exists")
        return redirect(url_for("register_page"))
    users[email] = {"name": name, "password": password}
    session["user"] = email
    return redirect(url_for("index"))

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")
    user = users.get(email)
    if not user or user.get("password") != password:
        flash("Invalid credentials")
        return redirect(url_for("login_page"))
    session["user"] = email
    return redirect(url_for("index"))

@app.route("/submit", methods=["POST"])
def submit():
    if "user" not in session:
        flash("Please log in to submit")
        return redirect(url_for("login_page"))
    title = request.form.get("title")
    content = request.form.get("content")
    submissions.append({"title": title, "content": content, "author": session["user"]})
    return redirect(url_for("index"))

# Very small admin endpoint to list submissions as JSON (protect appropriately)
@app.route("/admin/submissions")
def admin_submissions():
    if session.get("user") != "admin@example.com":
        return jsonify({"error": "forbidden"}), 403
    return jsonify(submissions)

if __name__ == "__main__":
    app.run(debug=True, port=5000)