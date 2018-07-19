import logging
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String
from werkzeug.security import generate_password_hash, check_password_hash
from UserService import app, db, data


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(64), index=True, unique=True)
    email = db.Column(String(120), index=True, unique=True)
    password_hash = db.Column(String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    def to_json(self):
        return dict(id=self.id,
                    username=self.username,
                    email=self.email,
                    password_hash=self.password_hash)

    def setPassword(password):
        password_hash = generate_password_hash(password)
        return password_hash

    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)
