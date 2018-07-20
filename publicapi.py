from flask import Flask
from werkzeug.exceptions import NotFound, ServiceUnavailable
from werkzeug.security import generate_password_hash, check_password_hash
import json
from flask import render_template, redirect, url_for, request, jsonify, abort, make_response
import requests
from slackclient import SlackClient
import os
import logging
import yaml
import sys
from datetime import datetime, timedelta


def configRead():

    if os.path.isfile('config.yaml'):
        with open('config.yaml', 'r') as f:
            doc = yaml.load(f)
        config = {'slack': doc['slack'], 'dataUserStore': doc['dataUserStore'], 'dataEventStore': doc['dataEventStore'], 'publicapi': doc['publicapi'], 'userservice': doc['userservice'], 'eventservice': doc['eventservice'], 'logLevel': doc['logLevel']}
        return config
    else:
        sys.exit('No config file')


def setupLogger(logLevel='INFO', filename='execution.log'):

    logging.basicConfig(filename=filename, format='%(asctime)s, %(message)s')
    logging.getLogger().setLevel(logLevel)
    return setupLogger


def root_dir():
    """ Returns root directory for this project """
    return os.path.dirname(os.path.realpath(__file__))


def nice_json(arg):
    response = make_response(json.dumps(arg, sort_keys=False, indent=4))
    response.headers['Content-type'] = "application/json"
    return response


def dateFormatOut(date_in):
    date_processing = date_in.replace('T', '-').replace(':', '-').split('-')
    date_processing = [int(v) for v in date_processing]
    date_out = datetime(*date_processing)
    return date_out


def dateFormatIn(date_in):

    switcher = {
        'Jan': '01',
        'Feb': '02',
        'Mar': '03',
        'Apr': '04',
        'May': '05',
        'Jun': '06',
        'Jul': '07',
        'Aug': '08',
        'Sep': '09',
        'Oct': '10',
        'Nov': '11',
        'Dec': '12'
    }

    date_processing = date_in[5:]
    date_processing = date_processing.replace(' GMT', '').replace(' ', '-').replace(',', '').replace(':', '-').split('-')
    switch = switcher.get(date_processing[1])
    date_processing[1] = switch
    date_out = datetime(int(date_processing[2]), int(date_processing[1]), int(date_processing[0]), int(date_processing[3]), int(date_processing[4]), int(date_processing[5]))
    return date_out


def dateComparison(startDate, endDate):
    if startDate > datetime.now():
        return 'incoming_events'
    elif endDate < datetime.now():
        return 'past_events'
    else:
        return 'current_events'


app = Flask(__name__)
slack_token = configRead()['slack']['SLACK_API_TOKEN']
sc = SlackClient(slack_token)


def notificationSlack(event):
    sc.api_call(
        "chat.postMessage",
        channel=configRead()['slack']['channel'],
        text="Your event {} is about to start".format(event))


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

    incoming_events = []
    current_events = []
    past_events = []
    urgent = []
    for event in output['events']:
        startDate = dateFormatIn(event['startDate'])
        endDate = dateFormatIn(event['endDate'])
        sortEvent = dateComparison(startDate, endDate)
        if sortEvent == 'current_events':
            current_events.append(event)
        elif sortEvent == 'incoming_events':
            incoming_events.append(event)
        elif sortEvent == 'past_events':
            past_events.append(event)

    for event in current_events:
        delta = (dateFormatIn(event['endDate']) - datetime.now())
        if delta < timedelta(days=2):
            urgent.append(event)
            notificationSlack(event['title'])

    return render_template('profile.html', username=user, incoming_events=incoming_events, current_events=current_events, past_events=past_events, urgent=urgent)


@app.route('/<username>/events/add', methods=['GET', 'POST'])
def addEvent(username):
    error = None
    if request.method == 'POST':
        startDate = dateFormatOut(request.form['startDate'])
        endDate = dateFormatOut(request.form['endDate'])
        if request.form.get('recurrence') == 'on':
            recurrence = True
        else:
            recurrence = False
        user = requests.post("http://localhost:5002/events?title=" + request.form['title'] + "&content=" + request.form['content'] + "&startDate=" + str(startDate) + "&endDate=" + str(endDate) + "&recurrence=" + str(recurrence) + "&user=" + username)
        return redirect('/{}/events'.format(username))
    return render_template('add-events.html')


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


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


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
