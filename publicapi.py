from flask import Flask
from werkzeug.exceptions import NotFound, ServiceUnavailable
import json
from flask import redirect, url_for, request, jsonify, abort, make_response
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
    return "<h1>welcome in the Event scheduler</h1>"


@app.route("/<user>/events", methods=['GET'])
def user(user):

    urls = [
        "http://127.0.0.1:5001/users/{}".format(user),
        "http://127.0.0.1:5002/events/{}".format(user)
    ]
    response = {}
    responses = []
    for u in urls:
        response = requests.get(u)
        response = response.json()
        responses.append(response)
    output = {'user': responses[0], 'events': responses[1]}

    return jsonify(output)


if __name__ == "__main__":
    app.run(port=configRead()['publicapi']['port'], debug=configRead()['publicapi']['debug'])
