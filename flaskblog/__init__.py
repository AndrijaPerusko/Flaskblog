from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flaskblog.config import Config


db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)

    from flaskblog.users import bp as users_bp
    app.register_blueprint(users_bp)

    from flaskblog.main import bp as main_bp
    app.register_blueprint(main_bp)

    from flaskblog.posts import bp as posts_bp
    app.register_blueprint(posts_bp)

    return app
