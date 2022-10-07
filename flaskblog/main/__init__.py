from flask import Blueprint

bp = Blueprint('main',__name__)

from flaskblog.main import routes
