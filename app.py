from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "secret123"

def connect():
    return sqlite3.connect("database.db")

conn = connect()
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)")
cursor.execute("CREATE TABLE IF NOT EXISTS projects(id INTEGER PRIMARY KEY, title TEXT, assigned_to INTEGER, status TEXT, submission TEXT)")
conn.commit()
conn.close()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = 'programmer'

        conn = connect()
        c = conn.cursor()
        c.execute("INSERT INTO users(username,password,role) VALUES(?,?,?)", (username,password,role))
        conn.commit()
        conn.close()

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = connect()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=? AND password=?", (username,password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = user
            if user[3] == 'admin':
                return redirect('/admin')
            return redirect('/dashboard')

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT * FROM projects WHERE assigned_to=?", (session['user'][0],))
    assigned = c.fetchall()
    conn.close()

    return render_template('dashboard.html', projects=assigned)

@app.route('/submit/<int:id>', methods=['GET','POST'])
def submit(id):
    if request.method == 'POST':
        submission = request.form['submission']

        conn = connect()
        c = conn.cursor()
        c.execute("UPDATE projects SET submission=?, status='submitted' WHERE id=?", (submission,id))
        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('submit.html', id=id)

@app.route('/admin', methods=['GET','POST'])
def admin():
    if 'user' not in session or session['user'][3] != 'admin':
        return redirect('/login')

    conn = connect()
    c = conn.cursor()
    c.execute("SELECT id, username FROM users WHERE role='programmer'")
    programmers = c.fetchall()
    c.execute("SELECT * FROM projects")
    projects = c.fetchall()
    conn.close()

    return render_template('admin.html', programmers=programmers, projects=projects)

@app.route('/assign', methods=['POST'])
def assign():
    title = request.form['title']
    programmer = request.form['programmer']

    conn = connect()
    c = conn.cursor()
    c.execute("INSERT INTO projects(title,assigned_to,status,submission) VALUES(?,?,?,?)", (title,programmer,'assigned',''))
    conn.commit()
    conn.close()

    return redirect('/admin')

app.run(debug=True)
