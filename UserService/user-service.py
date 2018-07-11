from flask import Flask
from flask_login import LoginManager, UserMixin, current_user, login_user, logout_user
from sqlalchemy.orm import sessionmaker, exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash


# Engine creation to connect the database
engine = create_engine('sqlite:///D:\\Event_Scheduler\\UserService\\users.db', echo=True)
# Declare a mapping of the base
Base = declarative_base()
# Table schema to create it
Base.metadata.create_all(engine)
#  Establishing a SQLAlchemy session
Session = sessionmaker(bind=engine)
session = Session()


# User Schema
class User(UserMixin, Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(64), index=True, unique=True)
    email = Column(String(120), index=True, unique=True)
    password_hash = Column(String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)

    # Create User
    def createUser(user):
        try:
            session.add(user)
            session.commit()
            print('New user created')
        except IntegrityError:
            print('Username or email already used')
            session.rollback()

    # Modify email address
    def updateUserEmail(currentUsername, newUserEmail):
        try:
            query = session.query(User)
            user = query.filter(User.username == currentUsername).first()
            user.email = newUserEmail
            session.commit()
            print('Email address updated')
        except AttributeError:
            print('User not found')

    # Modify password
    def updateUserPassword(currentUsername, currentPassword, newUserPassword):
        try:
            query = session.query(User)
            user = query.filter(User.username == currentUsername).first()
            if check_password_hash(user.password_hash, currentPassword):
                user.password_hash = generate_password_hash(newUserPassword)
                session.commit()
                print('Password updated')
            else:
                print('Invalid password')
        except AttributeError:
            print('User not found')

    # Delete user
    def deleteUser(username):
        try:
            query = session.query(User)
            query = query.filter(User.username == username)
            userToDelete = query.one()
            session.delete(userToDelete)
            session.commit()
        except NoResultFound:
            print('User not found')


# Authentification handler

# user1 = User('Alex', 'Alex@gmail.com', 'pass123')
# User.createUser(user1)
# User.updateUserPassword('Max', 'pass123', 'pass456')
# User.updateUserEmail('Max', 'maxime@gmail.com')
# User.deleteUser('Max')
