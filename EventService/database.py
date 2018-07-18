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
