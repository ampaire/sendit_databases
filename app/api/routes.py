from flask import Flask, request, session, jsonify, make_response, url_for
from app.models import User
from app.database import Database
from app import app
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

db = Database()


@app.route('/')
def index():
    return '<h2> Welcome to sendIt. Happy browsing</h2>'


@app.route('/api/v1/auth/signup', methods=['POST'])
def register_new_user():
    """route to sign up a new user to use the sendIt application"""

    response = request.get_json()
    userId = 0
    username = response.get("username")
    email = response.get("email")
    email = response.get("email")
    password = response.get("password")
    password = User.create_a_password_for_a_user(password)

    # validations

    db.register_user(username, email, password)
    return jsonify({"message": "user created"})


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or email.isspace():
        return jsonify({
            'message': 'Email is not valid. Enter a valid email.'
        }), 400
    if not password or password.isspace():
        return jsonify({
            'message': 'Password does not match with the entered email.'
        }), 400

    db = Database()
    user = db.login_a_user(email, password)

    if check_password_hash(user[3], password) and user[1] == email:
        access_token = create_access_token(identity=email)
        return jsonify({'token': access_token, 'message': ' Successfully logged in as {}'.format(email)
                        }), 200
    else:
        return jsonify({'message': 'Wrong login credentials.'}), 400
