from flask import Flask, request, session, jsonify, make_response, url_for
from sendit.models import User, ParcelOrder
from sendit.functions import check_validity_of_input, check_validity_of_mail, check_validity_of_username
from sendit.database import Database
from sendit import app, jwt, users
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash

db = Database()
db.create_tables()


@app.route('/')
def index():
    return 'Welcome to sendIt. Happy browsing'

#Register a user
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

    if db.get_user_by_email(email):
        return jsonify({'message':'User with that email already exists', "Status":"Failure"})

    if check_validity_of_input(username=username, email=email, password=password) == False:
        return jsonify({'message': 'Some fields are empty', "status":"Failure"}), 400

    if check_validity_of_mail(email) == None:
        return jsonify({'message': 'Invalid email format!', "status":"Failure"}), 400

    if len(username) < 3:
        return jsonify({'message':'Username is too short', "status":"Failure"}), 400

    registered_user = db.get_user(username, email, password)
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

    db = Database()
    user = db.get_logged_in_user(email, password)
    Access_token = create_access_token(identity=email)

    return jsonify({'Access_token': Access_token, "message": "successfully logged in", 'status':'Success'}), 200

#get parcel all users
@app.route('/api/v1/users', methods=["GET"])
@jwt_required
def get_all_users():
    if db.get_users():
        return jsonify({"Status":"Success", 'response':db.get_users()})
    return jsonify({'message':'No users have registered', "Status":"Failure"})

@app.route('/api/v1/auth/logout/<int:user>')

#add a parcel delivery order
@app.route('/api/v1/parcels', methods=['POST'])

def create_parcel_delivery_order():
    """
    register new parcel delivery order
    """
    data = request.get_json(force=True)

    if not data:
        return jsonify({'message': 'Cannot create parcel, some fields are missing', "status":"Failure"}), 400

    if (len(data.keys()) != 4):
        return jsonify({'message': 'Cannot create parcel due to missing fields', "status":"Failure"}), 400

    pickup_location = data['pickup_location']
    recipient = data['recipient']
    destination = data['destination']
    description = data['description']

    if len(description) < 5:
        return jsonify ({'message':'Please provide an elaborate parcel description', "status":"Failure"}),400

    parcel = ParcelOrder(
        pickup_location=pickup_location,
        recipient=recipient,
        destination=destination,
        description=description)

    

    db.post_new_order(pickup_location, destination,recipient, description)

    return jsonify({'message':'Parcel order successfully created', "status":"Success"}), 201

@app.route('/api/v1/parcels', methods = ['GET'])
@jwt_required
def get_all_orders():
    if db.get_all_parcels():
        return jsonify({"Status":"Success", 'response':db.get_all_parcels()}), 200
    return jsonify({'message':'No parcels have been added', "Status":"Failure"}), 404

#get one parcel delivery order
@app.route('/api/v1/parcels/<int:parcelId>', methods=['GET'])
@jwt_required
def get_one_delivery_order(parcelId):
    """ get parcel by parcelId """
    logged_in_user = get_jwt_identity()
    parcel = db.get_one_parcel(parcelId)
    if parcel:
        return jsonify(parcel), 200
    return jsonify({'message':'Cannot find parcel with that Id!','Status':'Failure'}), 400


#Cancel the status of a specific parcel delivery order
@app.route('/api/v1/parcels/<int:parcelId>/cancel', methods=['PUT'])
@jwt_required
def update_status(parcelId):
    """
    cancel status of a parcel delivery order
    """
    data = request.get_json()
    status = data.get("status")
    parcel = db.update_parcel_order_status(parcelId,status)
    if parcel:
        user_info = get_jwt_identity()
        if not parcel['userId'] == user_info['userId']:
            return jsonify({"message":"You cannot update the status of this parcel", "status":"Failure"}), 401
    return jsonify({"message":"Parcel succesfully cancelled", "status":"Success", "response":"Parcel Order status updated" }), 200
    # return jsonify({"message":"No parcel exists under that Id", "status":"Failure"}), 400

#Change the destination of a specific parcel delivery order
# @app.route('/api/v1/parcels/<int:parcelId>', methods= ['PUT'])
# @jwt_required
# def update_destination(parcelId):
#     """
#     Update the destination of a parcel delivery order
#     """
#     parcel = db.update_parcel_destination(parcelId)
#     if parcel:
#         current_user = get_jwt_identity()
#         if not parcel['userId']== current_user['userId']:
#             return jsonify({"message":"You cannot update the destination of this parcel", "status":"Failure"}), 401

#         if check_validity_of_input(destination=destination) == False:
#             return jsonify({'message':'The destination field cannot be left empty', "status":"Failure"}), 400
#         db.update_parcel_destination(parcel)
#         return jsonify ({"message":""})
            
#Change the present location of a specific parcel delivery order