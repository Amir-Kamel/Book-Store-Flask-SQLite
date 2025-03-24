from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_wtf.csrf import CSRFProtect
from config import Config
from flask_migrate import Migrate
from flask_login import LoginManager, current_user

db = SQLAlchemy()
csrf = CSRFProtect()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    Bootstrap(app)
    csrf.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @app.context_processor
    def inject_user():
        return dict(current_user=current_user)


    from app.authandbooks.routes import authandbooks
    from app.users.routes import users

    @app.before_request
    def restrict_access():
        allowed_routes = ['users.login', 'users.register', 'authandbooks.book_list', 'static']  # Allowed pages
        if not current_user.is_authenticated and request.endpoint not in allowed_routes:
            return redirect(url_for('users.login'))

    app.register_blueprint(authandbooks, url_prefix="/")
    app.register_blueprint(users, url_prefix="/user")

    with app.app_context():
        db.create_all()

    return app