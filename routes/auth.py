
import sqlite3
import re

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)
from flask_bcrypt import Bcrypt

auth_bp = Blueprint("auth", __name__)
bcrypt = Bcrypt()


def get_db():
    conn = sqlite3.connect(current_app.config["DATABASE_PATH"])
    conn.row_factory = sqlite3.Row
    return conn


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not name or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email):
        return jsonify({"error": "Invalid email address"}), 400

    if len(password) < 8:
        return jsonify({"error": "Password must be at least 8 characters"}), 400

    hashed_password = bcrypt.generate_password_hash(
        password
    ).decode("utf-8")

    conn = get_db()

    try:
        conn.execute(
            """INSERT INTO users (name, email, password)
               VALUES (?, ?, ?)""",
            (name, email, hashed_password)
        )
        conn.commit()

        return jsonify({
            "message": "Registration successful"
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({"error": "Email already registered"}), 409

    finally:
        conn.close()


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_db()

    try:
        user = conn.execute(
            "SELECT * FROM users WHERE email = ?",
            (email,)
        ).fetchone()
    finally:
        conn.close()

    if not user or not bcrypt.check_password_hash(
        user["password"], password
    ):
        return jsonify({"error": "Invalid email or password"}), 401

    token = create_access_token(identity=str(user["id"]))

    return jsonify({
        "message": "Login successful",
        "access_token": token,
        "token_type": "Bearer"
    }), 200


@auth_bp.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    user_id = get_jwt_identity()

    conn = get_db()

    try:
        user = conn.execute(
            "SELECT id, name, email FROM users WHERE id = ?",
            (user_id,)
        ).fetchone()
    finally:
        conn.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "message": "Access granted",
        "user": dict(user)
    }), 200
