from flask import Flask, make_response
from werkzeug.exceptions import NotFound, ServiceUnavailable
import json
import requests
import os
import logging
import yaml
import sys


def configRead():

    if os.path.isfile('config.yaml'):
        with open('config.yaml', 'r') as f:
            doc = yaml.load(f)
        config = {'dataUserStore': doc['dataUserStore'], 'dataEventStore': doc['dataEventStore'], 'publicapi': doc['publicapi'], 'userservice': doc['userservice'], 'eventservice': doc['eventservice'], 'logLevel': doc['logLevel']}
        return config
    else:
        sys.exit('No config file')


def setupLogger(logLevel='INFO', filename='execution.log'):

    logging.basicConfig(filename=filename, format='%(asctime)s, %(message)s')
    logging.getLogger().setLevel(logLevel)
    return setupLogger


app = Flask(__name__)


def root_dir():
    """ Returns root director for this project """
    return os.path.dirname(os.path.realpath(__file__))


def nice_json(arg):
    response = make_response(json.dumps(arg, sort_keys=False, indent=4))
    response.headers['Content-type'] = "application/json"
    return response


@app.route("/", methods=['GET'])
def index():
    return nice_json({
        "user": "/",
        "user_event": {
            "title": "/users/event",
            "description": "/users/",
            "start_date": "/users/",
            "end_date": "/users/"
        }
    })


@app.route("/users", methods=['GET'])
def users_list():
    return nice_json(users)


@app.route("/users/<username>", methods=['GET'])
def user_record(username):
    if username not in users:
        raise NotFound

    return nice_json(users[username])


if __name__ == "__main__":
    app.run(port=configRead()['publicapi']['port'], debug=configRead()['publicapi']['debug'])
