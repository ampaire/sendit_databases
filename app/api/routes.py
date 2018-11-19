from flask import Flask, request, session, jsonify, make_response, url_for
from app.models import *
from app.database import Database

db= Database()

@app.route('/')
def index():
    return '<h2> Welcome to sendIt. Happy browsing</h2>'


@app.route('/api/v1/auth/signup', methods=['POST'])
def register_new_user():
    """route to sign up a new user to use the sendIt application"""

    response = request.get_json()
    userId = 4
    username = response.get("username")
    email = response.get("email")
    password = response.get("password")
    password = generate_password_hash(password)
    role = respone.get ("role")

    # validations

    db.register_user(userId, username, email, password, role)
    return jsonify({"message":"user created"})




