from UserService import app, db, restAPI, data, database
from flask import redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from flask_restful import Resource
from requests import put, get


@app.route("/", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    return 'Welcome in the Event Scheduler app'


class getUser(Resource):
    def get(self, username):
        user = database.getUser(username)
        if user is None:
            return {'user': 'Not found'}
        else:
            return {'user': {
                'user': user.username,
                'email': user.email,
                'id': user.id,
            }}

    def put(self, username):
        return


restAPI.add_resource(getUser, '/user/<string:username>')


@app.route("/login", methods=['GET', 'POST'])
def login():

    return ('Hi !' + 'You are now logged in')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route("/register", methods=['GET', 'POST'])
def register():
    user = data.User('harry', 'harry@gmail.com', 'harry')
    response = database.saveUser(user)
    if response is True:
        return (user.username + " has been added to the app")
    else:
        return ('Username or email already used')


@app.route("/delete", methods=['GET', 'POST'])
def delete():
    user = 'mike'
    response = database.deleteUser(user)
    if response is True:
        return (user + " has been removed from the app")
    else:
        return 'User not found'


@app.route("/update/email", methods=['GET', 'POST'])
def emailUpdate():
    username = 'bill'
    newUserEmail = 'bob@gmail.com'
    response = database.updateUserEmail(username, newUserEmail)
    if response is True:
        return (username + "'s email has been modified")
    else:
        return 'User or email not found'


@app.route("/update/password", methods=['GET', 'POST'])
def passwordUpdate():
    username = 'bob'
    currentPassword = 'bob'
    newUserPassword = 'bob2'

    response = database.updateUserPassword(username, currentPassword, newUserPassword)
    if response is True:
        return (username + "'s password has been modified")
    else:
        return 'User not found or incorrect password'


@app.errorhandler(404)
def internal_error(error):
    return 'Error 404 - File not found'


@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return 'Error 500 - Internal Server Error'
