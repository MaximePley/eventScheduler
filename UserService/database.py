import logging
from UserService import db, data, login
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound


def saveUser(user):
    try:
        db.session.add(user)
        db.session.commit()
        logging.info('New user created')
        return True
    except IntegrityError:
        db.session.rollback()
        logging.info('Username or email already used')
        return False


def deleteUser(username):
    try:
        query = db.session.query(data.User)
        query = query.filter(data.User.username == username)
        userToDelete = query.one()
        db.session.delete(userToDelete)
        db.session.commit()
        logging.info('User deleted')
        return True
    except NoResultFound:
        logging.info('User not found')
        return False


def updateUserEmail(username, newUserEmail):
    try:
        query = db.session.query(data.User)
        query.filter(data.User.username == username).update({'email': newUserEmail})
        db.session.commit()
        logging.info('Email updated')
        return True
    except AttributeError:
        logging.info('User not found')
        return False


def updateUserPassword(username, currentPassword, newUserPassword):
    # try:
    query = db.session.query(data.User)
    user = query.filter(data.User.username == username).first()
    if data.User.checkPassword(user.password_hash, currentPassword):
        user.password_hash = data.User.setPassword(newUserPassword)
        db.session.commit()
        logging.info('Password updated')
        return True
    else:
        logging.info('Invalid password')
        return False
    # except AttributeError:
    #     print('User not found')
