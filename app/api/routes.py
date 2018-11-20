from flask import Flask, request, session, jsonify, make_response, url_for
from app.models import User
from app.database import Database
from app import app
from jwt-extended import jwt_required,

db= Database()

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
    password = response.get("password")
    password = User.create_a_password_for_a_user(password)
    role = respone.get ("role")

    # validations

    db.register_user(userId, username, email, password, role)
    return jsonify({"message":"user created"})

@app.route('/api/v1/auth/login', methods=['GET','POST'])
data =  request.get_json()
email = response.get('email')
password = response.get ('password')


logged_in_user= db.login_a_user(email,password)
if logged_in_user:
    return jsonify({"Access-token":create})






