import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.getenv("SECRET_KEY")

    SQLALCHEMY_DATABASE_URI = "sqlite:///trek.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    REDIS_URL = "redis://localhost:6379/0"

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

