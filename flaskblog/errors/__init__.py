from flask import Blueprint

bp = Blueprint('errors', __name__)

from flaskblog.errors import handlers
