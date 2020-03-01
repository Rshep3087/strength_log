import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = "5791628bb0b13ce0c676dfde280ba245"
    username = "rshep3087"
    password = "KJNqp6FkVnJc9ONTpaOT"
    hostname = "rshep3087.mysql.pythonanywhere-services.com"
    databasename = "rshep3087$strength_log"
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{username}:{password}@{hostname}/{databasename}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_POOL_RECYCLE = 299
