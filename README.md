# CodeIt

This repository contains a small Flask-based site (index.html, login, register, submit, admin, styles) and a minimal Flask server (app.py) to serve it.

Getting started locally

1. Create a virtual environment and activate it:

   python3 -m venv .venv
   source .venv/bin/activate

2. Install requirements:

   pip install -r requirements.txt

3. (Optional) Copy .env.example to .env and set SECRET_KEY

4. Run the app:

   python app.py

5. Open http://localhost:5000

Using Docker

Build and run with docker-compose:

   docker-compose up --build

Or build the image manually and run:

   docker build -t codeit .
   docker run -p 5000:5000 --env SECRET_KEY=change-me codeit

Deploying to Heroku / Render

- The included Procfile and runtime.txt make it straightforward to deploy to Heroku. Set environment variable SECRET_KEY in the platform and install required packages.

Security & next steps

- Replace SECRET_KEY with a secure random value and store it in environment variables.
- Swap in a real database (SQLite/Postgres) and hash passwords with bcrypt (passlib).
- Add CSRF protection (Flask-WTF) and proper role-based auth for admin.
