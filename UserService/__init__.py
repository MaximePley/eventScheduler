import os
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
api = Api(app)

# Default config
app.config.update(
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.getcwd() + '\\UserService\\user.db'
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

from UserService import api, data, database
