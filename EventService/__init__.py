import os
import publicapi
from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager


app = Flask(__name__)
restAPI = Api(app)
app.config['JSON_SORT_KEYS'] = False

# Default config
app.config.update(
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.getcwd() + publicapi.configRead()['dataEventStore']['fileName']
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

from EventService import api, data, database
