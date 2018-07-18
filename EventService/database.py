import logging
from EventService import db, data
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


def getEvent(event_id):
    try:
        query = db.session.query(data.Event)
        query = query.filter(data.Event.id == event_id).first()
        return query
    except AttributeError:
        logging.info('Event not found')
        return False


def getAllEvents():
    query = db.session.query(data.Event).all()
    return query


def getEventByUser(user):
    query = db.session.query(data.Event)
    query = query.filter(data.Event.user == user).all()
    return query


def saveEvent(event):
    try:
        db.session.add(event)
        db.session.commit()
        logging.info('New event created')
        return True
    except IntegrityError:
        db.session.rollback()
        logging.info('Event input problem')
        return False


def deleteEvent(event_id):
    try:
        query = db.session.query(data.Event)
        query = query.filter(data.Event.id == event_id)
        eventToDelete = query.one()
        db.session.delete(eventToDelete)
        db.session.commit()
        logging.info('Event deleted')
        return True
    except NoResultFound:
        logging.info('Event not found')
        return False


def deleteEventbyUser(user):
    query = db.session.query(data.Event)
    query = query.filter(data.Event.user == user).delete()
    db.session.commit()


def updateEventTitle(event_id, newEventTitle):
    try:
        query = db.session.query(data.Event)
        query.filter(data.Event.id == event_id).update({'title': newEventTitle})
        db.session.commit()
        logging.info('Title updated')
        return True
    except AttributeError:
        logging.info('Event not found')
        return False


def updateEventRecurrenceByUser(user, recurrence):
    query = db.session.query(data.Event)
    events = query.filter(data.Event.user == user).update({'recurrence': recurrence})
    db.session.commit()
    logging.info('Recurrence updated')
