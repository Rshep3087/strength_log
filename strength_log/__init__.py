from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from strength_log.config import Config
from loguru import logger


# configuration

db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()
login.login_view = "users.login"
login.login_message_category = "info"
migrate = Migrate()


# app factory
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    logger.info("App init")

    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)
    migrate.init_app(app, db=db)

    from strength_log.users.routes import users
    from strength_log.posts.routes import posts
    from strength_log.main.routes import main
    from strength_log.maxes.routes import maxes

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(maxes)

    return app
