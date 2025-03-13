from flask import Blueprint

authandbooks = Blueprint('authandbooks', __name__, template_folder="templates")

from app.authandbooks import routes