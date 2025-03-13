import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '44f6c84390d56356963c706c3ee43059'
    UPLOAD_FOLDER = 'static/images/'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    DB_PATH = os.path.join(BASE_DIR, "instance", "database.db")

    if os.getenv("FLY_IO"):
        SQLALCHEMY_DATABASE_URI = "sqlite:////data/database.db"
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"
