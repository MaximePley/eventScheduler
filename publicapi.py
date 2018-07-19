from flask import Flask
from werkzeug.exceptions import NotFound, ServiceUnavailable
from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask import render_template, redirect, url_for, request, jsonify, abort, make_response
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


def root_dir():
    """ Returns root director for this project """
    return os.path.dirname(os.path.realpath(__file__))


def nice_json(arg):
    response = make_response(json.dumps(arg, sort_keys=False, indent=4))
    response.headers['Content-type'] = "application/json"
    return response


app = Flask(__name__)


@app.route("/", methods=['GET'])
def index():
    return "<h1>Welcome in the Event scheduler</h1>"


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


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        user = requests.get("http://localhost:5001/users/{}".format(username))
        password_hash = json.loads(user.text)["password_hash"]

        if not check_password_hash(password_hash, request.form['password']):
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect('/{}/events'.format(username))
    return render_template('login.html', error=error)


# Route for handling the login page logic
@app.route('/<username>/events', methods=['GET', 'POST'])
def events(username):
    error = None
    if request.method == 'POST':
        user = requests.post("http://localhost:5002/events?title=" + request.form['title'] + "&content=" + request.form['content'] + "&startDate=" + request.form['startDate'] + "&endDate=" + request.form['endDate'] + "&recurrence=" + request.form['recurrence'] + "&user=" + username)

        return redirect('/{}/events'.format(username))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


# Route for handling the login page logic
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        if request.form['password'] != request.form['password2']:
            error = 'Passwords dont match. Please try again.'
        else:
            requests.post("http://localhost:5001/register?username=" + request.form['username'] + "&email=" + request.form['email'] + "&password=" + request.form['password'])
            return redirect(url_for('login'))
    return render_template('register.html', error=error)


if __name__ == "__main__":
    app.run(port=configRead()['publicapi']['port'], debug=configRead()['publicapi']['debug'])
