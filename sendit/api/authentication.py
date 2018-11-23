from flask import Flask, request, session, jsonify, make_response, url_for
from sendit.models.user_models import User
from sendit.validators import  check_validity_of_mail, check_validity_of_username
from sendit.database import Database
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from sendit import app
from werkzeug.security import generate_password_hash, check_password_hash


@app.route('/api/v1/auth/signup', methods=['POST'])
def register_new_user():
    """route to sign up a new user to use the sendIt application"""

    response = request.get_json()
    if len(response.keys()) != 3:
        return jsonify({'message': 'Could not create user, with missing parameters', 'status':'Failure'}), 400

    username = response.get("username")
    email = response.get("email")
    password = response.get("password")
    password = User.create_a_password_for_a_user(password)

    if User.get_user_by_email(email):
        return jsonify({'message':'User with that email already exists', "Status":"Failure"})


    if check_validity_of_mail(email) == None:
        return jsonify({'message': 'Invalid email format!', "status":"Failure"}), 400

    if len(username) < 3:
        return jsonify({'message':'Username is too short', "status":"Failure"}), 400

    registered_user = User().post_user(username, email, password)
    return jsonify ({'message': 'You successfully created your account!', 'status': 'Successful'}), 201

#login a user
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request", "status":"Failure"}), 400

    data = request.json
    email = data.get('email', None)
    password = data.get('password', None)

    if not email:
        return jsonify({"message": "Missing email parameter", "status":"Failure"}), 400

    if not password:
        return jsonify({"message": "Missing password parameter", "status":"Failure"}), 400

    if email == '' or password == '':
        return jsonify({"message": "Bad email or password", "status":"Failure"}), 401

    User.get_logged_in_user(email, password)
    Access_token = create_access_token(identity=email)

    return jsonify({'Access_token': Access_token, "message": "successfully logged in", 'status':'Success'}), 200
