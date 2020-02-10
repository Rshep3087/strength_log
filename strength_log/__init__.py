from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# from flask_migrate import Migrate

######################
### Configuration ####
######################
db = SQLAlchemy()
bcrypt = Bcrypt()
login = LoginManager()
login.login_view = "user.login"

#################
#### Logging ####
#################

from loguru import logger

#####################
#### App Factory ####
#####################


def create_app(config_filename=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile(config_filename)
    initialize_extensions(app)
    register_blueprints(app)
    logger.info("App init")
    return app


def initialize_extensions(app: Flask):
    db.init_app(app)
    bcrypt.init_app(app)
    login.init_app(app)


def register_blueprints(app: Flask):
    from strength_log.users import users_blueprint

    app.register_blueprint(users_blueprint)


# from strength_log import routes
