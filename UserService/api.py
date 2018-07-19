from UserService import app, db, restAPI, data, database
from flask import redirect, url_for, request, jsonify, abort, make_response
from flask_login import current_user, login_user, logout_user, login_required
from flask_restful import Resource


@app.route("/", methods=['GET'])
@app.route("/index", methods=['GET'])
def index():
    return 'Welcome in the User service app'


@app.route("/register", methods=['GET', 'POST'])
def users():
    if request.method == "POST":
        username = request.args.get('username')
        email = request.args.get('email')
        password = request.args.get('password')
        user = data.User(username, email, password)
        database.saveUser(user)
        obj = data.User.to_json(user)
        response = jsonify(obj)
        response.status_code = 201
        return response
    else:
        # GET
        users = database.getAllUsers()
        results = []

        for user in users:
            obj = data.User.to_json(user)
            results.append(obj)
        response = jsonify(results)
        response.status_code = 200
        return response


@app.route('/users/<username>', methods=['GET', 'PUT', 'DELETE'])
def user(username):
    user = database.getUser(username)
    if not user:
        # Raise an HTTPException with a 404 not found status code
        abort(404)

    if request.method == 'DELETE':
        database.deleteUser(username)
        return (
            "User {} deleted successfully".format(user.username)
        ), 200

    elif request.method == 'PUT':
        email = str(request.args.get('email', 'bobby@gmail.com'))
        database.updateUserEmail(username, email)
        obj = data.User.to_json(user)
        response = jsonify(obj)
        response.status_code = 200
        return response
    else:
        # GET
        obj = data.User.to_json(user)
        response = jsonify(obj)
        response.status_code = 200
        return response
