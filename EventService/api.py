from EventService import app, db, restAPI, data, database
from flask import redirect, url_for
from flask_restful import Resource
from requests import put, get
from datetime import datetime


@app.route("/", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    return 'Welcome in the Event Service app'


class getEvent(Resource):
    def get(self, event_id):
        event = database.getEvent(event_id)
        if event is None:
            return {'event': 'Not found'}
        else:
            start_date = str(datetime.strptime(str(event.startDate).split(".")[0], '%Y-%m-%d %H:%M:%S'))
            end_date = str(datetime.strptime(str(event.endDate).split(".")[0], '%Y-%m-%d %H:%M:%S'))
            return {'event': {
                'event_title': event.title,
                'event_content': event.content,
                'id': event.id,
                'start_date': start_date,
                'end_date': end_date,
                'recurrence': event.recurrence
            }}


restAPI.add_resource(getEvent, '/event/<string:event_id>')


@app.route("/addevent", methods=['GET', 'POST'])
def addEvent():
    event = data.Event('Finish app2', 'write API2', datetime.now(), datetime.now(), datetime.now(), False, 'user1')
    response = database.saveEvent(event)
    if response is True:
        return (event.title + " has been added to the app")
    else:
        return ('Event input error')


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    event_id = '2'
    response = database.deleteEvent(event_id)
    if response is True:
        return ("Event has been removed from the app")
    else:
        return 'Event not found'


@app.errorhandler(404)
def internal_error(error):
    return 'Error 404 - File not found'


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return 'Error 500 - Internal Server Error'
