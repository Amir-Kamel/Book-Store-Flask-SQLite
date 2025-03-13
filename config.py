import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or '44f6c84390d56356963c706c3ee43059'
    UPLOAD_FOLDER = 'static/images/'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    INSTANCE_DIR = os.path.join(BASE_DIR, "instance")

    # Ensure the instance directory exists locally
    if not os.getenv("FLY_IO"):
        os.makedirs(INSTANCE_DIR, exist_ok=True)

    DB_PATH = os.path.join(INSTANCE_DIR, "database.db")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_PATH}"