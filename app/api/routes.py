from flask import Flask, request, session, jsonify, make_response, url_for
from app.models import User, ParcelOrder
from app.functions import check_validity_of_input, check_validity_of_mail, check_validity_of_username
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

#Register a user
@app.route('/api/v1/auth/signup', methods=['POST'])
def register_new_user():
    """route to sign up a new user to use the sendIt application"""

    response = request.get_json()
    if len(response.keys()) != 3:
        return jsonify({'message': 'Could not create user, with missing parameters'}, {'status':'Failure'}), 400

    username = response.get("username")
    email = response.get("email")
    password = response.get("password")
    password = User.create_a_password_for_a_user(password)

    if 'email' in response.keys():
        email = response['email']
        return jsonify({'message': 'User with that email already exists'}, {"status":"Failure"})


    if check_validity_of_input(username=username, email=email, password=password) == False:
        return jsonify({'message': 'Some fields are empty'}, {"status":"Failure"}), 400

    if check_validity_of_mail(email) == None:
        return jsonify({'message': 'Invalid email format!'},{"status":"Failure"}), 400

    if len(username) < 3:
        return jsonify({'message':'Username is too short'}, {"status":"Failure"}), 400

    registered_user = db.register_user(username, email, password)
    return jsonify ({'message': 'You successfully created your account!'}, {'status': 'Successful'}, {"response": registered_user}), 201

#login a user
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    if not request.is_json:
        return jsonify({"message": "Missing JSON in request"}, {"status":"Failure"}), 400

    data = request.json
    email = data.get('email', None)
    password = data.get('password', None)

    if not email:
        return jsonify({"message": "Missing email parameter"},{"status":"Failure"}), 400

    if not password:
        return jsonify({"message": "Missing password parameter"},{"status":"Failure"}), 400

    if email == '' or password == '':
        return jsonify({"message": "Bad email or password"}, {"status":"Failure"}), 401

    db = Database()
    user = db.login_a_user(email, password)
    Access_token = create_access_token(identity=email)

    return jsonify({'Access_token': Access_token}, {"message": "successfully logged in"}, {'status':'Success'}), 200

#get parcel all users
@app.route('/api/v1/users', methods=["GET"])
@jwt_required
def get_all_users():
    current_user = get_jwt_identity()
    if current_user == "admin@sendit.com":
        db = Database
        if users:
            return db.get_all_availabe_users(username, email), 200
        else:
            return jsonify({'message', 'No data to display, No users have registered'}, {"status":"Failure"}), 404
    return jsonify({'message', 'Not authorised'}, {"status":"Failure"}), 403

@app.route('/api/v1/auth/logout/<int:user>')

#add a parcel delivery order
@app.route('/api/v1/parcels', methods=['POST'])

def create_parcel_delivery_order():
    """
    register new parcel delivery order
    """
    data = request.get_json(force=True)

    if not data:
        return jsonify({'message': 'Cannot create parcel, some fields are missing'}, {"status":"Failure"}), 400

    if (len(data.keys()) != 4):
        return jsonify({'message': 'Cannot create parcel due to missing fields'}, {"status":"Failure"}), 400

    pickup_location = data['pickup_location']
    recipient = data['recipient']
    destination = data['destination']
    description = data['description']

    if check_validity_of_input(pickup_location=pickup_location, recipient=recipient, destination=destination,
                               description=description) == False:

        return jsonify({'message', 'Some fields are empty'}, {"status":"Failure"}), 400

    if len(description) < 5:
        return jsonify ({'message':'Please provide an elaborate parcel description'}, {"status":"Failure"}),400

    parcel = ParcelOrder(
        pickup_location=pickup_location,
        recipient=recipient,
        destination=destination,
        description=description)

    new_parcel = db.post_new_order(pickup_location, destination,recipient, description)
    return jsonify({'message':'Parcel order successfully created'},{"status":"Success"}), 201
#get all parcel delivery orders
@app.route('/api/v1/parcels', methods = ['GET'])
@jwt_required
def get_all_orders():
    pass

#Change the status of a specific parcel delivery order
@app.route('/api/v1/parcels/<int:orderID>/cancel', methods=['PUT'])
@jwt_required
def parcelOrder(orderID):
    """ cancelling status of a parcel delivery order"""
    parcel = database.getoneparcel(parcelId)
    if parcel:
        user_info = get_jwt_identity()
        if not parcel['userid'] == user_info['userid']:
            return jsonify({"message":"Rights to update denied"}), 401
        parcel['status'] = 'Cancelled'
        db.update_parcel_order(parcel)
        return jsonify(parcel), 200
return jsonify({"message":"No parcel exists under that Id"}, {"status":"Failure"}) 400

#get one parcel delivery order

#Change the destination of a specific parcel delivery order


#Change the present location of a specific parcel delivery order