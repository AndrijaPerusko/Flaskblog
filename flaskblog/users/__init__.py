from flask import Blueprint

bp = Blueprint('users', __name__)

from flaskblog.users import routes
