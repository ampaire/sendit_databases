from flask import Flask, request, session, jsonify, make_response, url_for
from app.models import User, ParcelOrder
from app.functions import json_response, check_validity_of_input
from app.database import Database
from app import app, jwt, users
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

db = Database()
db.create_tables()
db.drop_tables()


@app.route('/')
def index():
    return 'Welcome to sendIt. Happy browsing'


@app.route('/api/v1/auth/signup', methods=['POST'])
def register_new_user():
    """route to sign up a new user to use the sendIt application"""

    response = request.get_json()
    userId = 0
    username = response.get("username")
    email = response.get("email")
    password = response.get("password")
    password = User.create_a_password_for_a_user(password)
    if check_validity_of_input(username=username, email=email, password=password) == False:
        return jsonify({'message', 'Some fields are empty'}, {"status":"Failed"}), 400

    registered_user = db.register_user(username, email, password)
    return jsonify ({'message': 'You successfully created your account!'}, {'status': 'Successful'}, {"data": registered_user}), 201


@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400
    data = request.json
    email = data.get('email', None)
    password = data.get('password', None)
    if not email:
        return jsonify({"msg": "Missing email parameter"}), 400
    if not password:
        return jsonify({"msg": "Missing password parameter"}), 400

    if email == '' or password == '':
        return jsonify({"msg": "Bad email or password"}), 401

    db = Database()
    user = db.login_a_user(email, password)
    Access_token = create_access_token(identity=email)
    return jsonify({'Access_token': Access_token}, {"message": "successfully logged in"}), 200


@app.route('/api/v1/users', methods=["GET"])
@jwt_required
def get_all_users():
    current_user = get_jwt_identity()
    if current_user == "admin@sendit.com":
        db = Database
        if users:
            return db.get_all_availabe_users(username, email), 200
        else:
            return json_response('message', 'No data to display, No users have registered'), 404
    return json_response('message', 'Not authorised'), 403


@app.route('/api/v1/parcels', methods=['POST'])

def create_parcel_delivery_order():
    """
    register new parcel delivery order
    """
    data = request.get_json(force=True)

    if not data:
        return json_response(
            'message', 'Cannot create parcel, some fields are missing'), 400

    if (len(data.keys()) != 4):
        return json_response(
            'message', 'Cannot create parcel due to missing fields'), 400

    pickup_location = data['pickup_location']
    recipient = data['recipient']
    destination = data['destination']
    description = data['description']

    if check_validity_of_input(pickup_location=pickup_location, recipient=recipient, destination=destination,
                               description=description) == False:
        return json_response('message', 'Some fields are empty'), 400

    parcel = ParcelOrder(
        pickup_location=pickup_location,
        recipient=recipient,
        destination=destination,
        description=description)

    new_parcel = db.post_new_order(pickup_location, destination,recipient, description)

    return jsonify({'message':'Parcel order successfully created'})

