from flask import Blueprint

bp = Blueprint('posts',__name__)

from flaskblog.posts import routes
