
import os
import sqlite3

from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from config import Config
from routes.auth import auth_bp, bcrypt


app = Flask(__name__)
app.config.from_object(Config)

bcrypt.init_app(app)
jwt = JWTManager(app)


def init_db():
    db_path = app.config["DATABASE_PATH"]
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project": "User Authentication & JWT",
        "status": "Backend Running Successfully",
        "endpoints": [
            "/api/auth/register",
            "/api/auth/login",
            "/api/auth/profile"
        ]
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "healthy"}), 200


app.register_blueprint(auth_bp, url_prefix="/api/auth")

# Initialize database even when launched using Gunicorn
init_db()


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", 5000)),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true"
    )
