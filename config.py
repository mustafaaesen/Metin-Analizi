import os

SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
SQLALCHEMY_TRACK_MODIFICATIONS = False
SECRET_KEY = os.environ.get("SECRET_KEY")

if not SQLALCHEMY_DATABASE_URI:
    raise RuntimeError("DATABASE_URL is not set")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is not set")
