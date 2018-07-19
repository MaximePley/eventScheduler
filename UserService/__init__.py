import os
import publicapi
from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
restAPI = Api(app)

# Default config
app.config.update(
    SQLALCHEMY_TRACK_MODIFICATIONS=False,
    SQLALCHEMY_DATABASE_URI='sqlite:///' + os.getcwd() + publicapi.configRead()['dataUserStore']['fileName']
)

db = SQLAlchemy(app)
migrate = Migrate(app, db)


from UserService import api, data, database
