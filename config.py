
import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    SECRET_KEY = os.getenv("FLASK_SECRET_KEY", JWT_SECRET_KEY)

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

    DATABASE_PATH = os.getenv(
        "DATABASE_PATH",
        os.path.join(BASE_DIR, "database", "users.db")
    )

    if not JWT_SECRET_KEY:
        raise RuntimeError("JWT_SECRET_KEY is missing")
