from flask import Blueprint

users = Blueprint('users', __name__, template_folder="templates")

from app.users import routes
