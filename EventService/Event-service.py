from datetime import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Date, Boolean, DateTime
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import OperationalError


# Engine creation to connect the database
engine = create_engine('sqlite:///D:\\Event_Scheduler\\EventService\\events.db', echo=True)
# Declare a mapping of the base
Base = declarative_base()
# Table schema to create it
Base.metadata.create_all(engine)
#  Establishing a SQLAlchemy session
Session = sessionmaker(bind=engine)
session = Session()


# Event Schema
class Event(Base):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), index=True)
    content = Column(String(500))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    startDate = Column(Date(), index=True)
    endDate = Column(Date(), index=True)
    recurrence = Column(Boolean)

    def __repr__(self):
        return '<Event {}>'.format(self.title)

    def __init__(self, title, content, timestamp, startDate, endDate, recurrence):
        self.title = title
        self.content = content
        self.timestamp = timestamp
        self.startDate = startDate
        self.endDate = endDate
        self.recurrence = recurrence

    # Create Event
    def createEvent(event):
        try:
            session.add(event)
            session.commit()
            print('New event created')
        except OperationalError:
            Base.metadata.create_all(engine)
            session.add(event)
            session.commit()
            print('New event created')

    # Modify event
    def updateEvent(currentTitle, newTitle, content, timestamp, startDate, endDate, recurrence):
        try:
            query = session.query(Event)
            event = query.filter(Event.title == currentTitle).first()
            event.title = newTitle
            event.content = content
            event.timestamp = timestamp
            event.startDate = startDate
            event.endDate = endDate
            event.recurrence = recurrence
            session.commit()
            print('Event updated')
        except AttributeError:
            print('Event not found')

    # Delete event
    def deleteEvent(title):
        try:
            query = session.query(Event)
            query = query.filter(Event.title == title).all()
            for q in query:
                session.delete(q)
                session.commit()
        except NoResultFound:
            print('Event not found')

##############################################################################


# event1 = Event('another3', 'description', datetime(2012, 3, 3, 10, 10, 10), datetime(2012, 3, 3, 10, 10, 10), datetime(2012, 3, 3, 10, 10, 10), True)
# Event.createEvent(event1)
# Event.updateEvent('another3', 'another50', 'description', datetime(2012, 3, 3, 10, 10, 10), datetime(2012, 3, 3, 10, 10, 10), datetime(2012, 3, 3, 10, 10, 10), False)
# Event.deleteEvent('another2')

##############################################################################
