import os

from dotenv import load_dotenv

load_dotenv()


class Config:

    SECRET_KEY = os.environ.get(
        "YPTSC_SECRET_KEY",
        "YPTSC-IMS-DEV-KEY"
    )

    # ==================================
    # POSTGRESQL
    # ==================================

    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ==================================
    # FLASK
    # ==================================

    TEMPLATES_AUTO_RELOAD = True

    SESSION_PERMANENT = False

    SESSION_COOKIE_HTTPONLY = True

    SESSION_COOKIE_SAMESITE = "Lax"

    SESSION_COOKIE_SECURE = False