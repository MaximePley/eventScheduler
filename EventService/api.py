from EventService import app, db, restAPI, data, database
from flask import redirect, url_for, request, jsonify, abort, make_response
from flask_restful import Resource
from requests import put, get
from datetime import datetime


@app.route("/", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    return 'Welcome in the Event Service app'


@app.route("/events", methods=['GET', 'POST'])
def events():
    if request.method == "POST":
        title = request.args.get('title')
        content = request.args.get('content')
        startDate = request.args.get('startDate')
        startDate = datetime.strptime(startDate, "%d-%m-%Y-%H:%M")
        endDate = request.args.get('endDate')
        endDate = datetime.strptime(endDate, "%d-%m-%Y-%H:%M")
        recurrence = bool(request.args.get('recurrence'))
        user = request.args.get('user')
        event = data.Event(title, content, datetime.now(), startDate, endDate, recurrence, user)
        database.saveEvent(event)
        obj = data.Event.to_json(event)
        response = jsonify(obj)
        response.status_code = 201
        return response
    else:
        # GET
        events = database.getAllEvents()
        results = []

        for event in events:
            obj = data.Event.to_json(event)
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response


@app.route('/event/<id>', methods=['GET', 'PUT', 'DELETE'])
def event(id):
    event = database.getEvent(id)
    if not event:
        # Raise an HTTPException with a 404 not found status code
        abort(404)

    if request.method == 'DELETE':
        database.deleteEvent(id)
        return (
            "Event {} deleted successfully".format(event.title)
        ), 200

    elif request.method == 'PUT':
        title = str(request.args.get('title', 'Modified title'))
        database.updateEventTitle(id, title)
        obj = data.Event.to_json(event)
        response = jsonify(obj)
        response.status_code = 200
        return response
    else:
        # GET
        obj = data.Event.to_json(event)
        response = jsonify(obj)
        response.status_code = 200
        return response


@app.route('/events/<user>', methods=['GET', 'PUT', 'DELETE'])
def eventByUser(user):
    events = database.getEventByUser(user)
    results = []
    if not events:
        # Raise an HTTPException with a 404 not found status code
        abort(404)

    if request.method == 'DELETE':
        database.deleteEventbyUser(user)
        return (
            "Event from {} deleted successfully".format(user)
        ), 200

    elif request.method == 'PUT':
        recurrence = True
        database.updateEventRecurrenceByUser(user, recurrence)
        for event in events:
            obj = data.Event.to_json(event)
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response
    else:
        # GET
        for event in events:
            obj = data.Event.to_json(event)
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response


@app.errorhandler(404)
def internal_error(error):
    return 'Error 404 - File not found'


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return 'Error 500 - Internal Server Error'
