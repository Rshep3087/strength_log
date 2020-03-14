from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from loguru import logger

from strength_log.config import Config


# configuration

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
mail = Mail()
login = LoginManager()
login.login_view = "users.login"
login.login_message_category = "info"


# app factory
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    logger.info("App init")

    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db=db)

    from strength_log.users.routes import users
    from strength_log.posts.routes import posts
    from strength_log.main.routes import main
    from strength_log.maxes.routes import maxes
    from strength_log.errors.routes import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(maxes)
    app.register_blueprint(errors)

    return app


app = create_app()
