from datetime import date, datetime
import logging
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from EventService import app, db, data


class Event(db.Model):
    __tablename__ = 'events'

    id = Column(Integer, primary_key=True)
    title = Column(String(120), index=True)
    content = Column(String(500))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    startDate = Column(DateTime, index=True)
    endDate = Column(DateTime, index=True)
    recurrence = Column(Boolean, default=True)
    user = Column(String(120))

    def __repr__(self):
        return '<Event {}>'.format(self.title)

    def __init__(self, title, content, timestamp, startDate, endDate, recurrence, user):
        self.title = title
        self.content = content
        self.timestamp = timestamp
        self.startDate = startDate
        self.endDate = endDate
        self.recurrence = recurrence
        self.user = user

    def to_json(self):
        return dict(id=self.id,
                    title=self.title,
                    content=self.content,
                    timestamp=self.timestamp,
                    startDate=self.startDate,
                    endDate=self.endDate,
                    recurrence=self.recurrence,
                    user=self.user)
