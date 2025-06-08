# app/main.py

import os
import psycopg2
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

# Read database URL from environment (set by docker-compose)
DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Return a database connection.

    Supports PostgreSQL via psycopg2 and SQLite for local testing when
    ``DATABASE_URL`` starts with ``sqlite://``.
    """
    url = os.getenv("DATABASE_URL", DATABASE_URL)
    if url and url.startswith("sqlite://"):
        path = url[len("sqlite://") :]
        return sqlite3.connect(path)
    return psycopg2.connect(url)

@app.route("/")
def index():
    return jsonify({"message": "Welcome to Dockerized Dev Env Template!"})

@app.route("/users")
def list_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, name, email FROM users;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    users = [{"id": r[0], "name": r[1], "email": r[2]} for r in rows]
    return jsonify(users)

@app.route("/health")
def health():
    try:
        conn = get_db_connection()
        conn.cursor().execute("SELECT 1;")
        conn.close()
        return jsonify({"status": "OK"}), 200
    except Exception:
        return jsonify({"status": "FAIL"}), 500

if __name__ == "__main__":
    # Use host="0.0.0.0" so Docker can route traffic
    app.run(host="0.0.0.0", port=5000)
