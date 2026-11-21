import os
import psycopg
from flask import Flask, jsonify

app = Flask(__name__)

@app.get("/")
def home():
    return jsonify({"message": "Kaa Store API aktif"})

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

@app.get("/db-check")
def db_check():
    db_url = os.getenv("DATABASE_URL") or os.getenv("STORAGE_URL")

    if not db_url:
        return jsonify({"database": "url_not_found"}), 500

    try:
        with psycopg.connect(db_url, connect_timeout=5) as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
                cur.fetchone()

        return jsonify({"database": "connected"})

    except Exception:
        app.logger.exception("Database connection failed")
        return jsonify({"database": "connection_failed"}), 500
