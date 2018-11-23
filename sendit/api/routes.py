from flask import Flask, request, session, jsonify
from sendit.models.user_models import User
from sendit.models.parcel_models import ParcelOrder
from sendit.validators import check_validity_of_input
from sendit.main import views
from sendit.database import Database
from sendit import app, jwt, users
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
from sendit import app

db = Database()
db.create_tables()

@app.route('/api/v1/users', methods=["GET"])
@jwt_required
def get_all_users():
    if User().get_users():
        return jsonify({"Status": "Success", 'response': User.get_users()}), 200
    return jsonify({'message': 'No users have registered', "Status": "Failure"}), 400


@app.route('/api/v1/auth/logout/<int:user>')
# add a parcel delivery order
@app.route('/api/v1/parcels', methods=['POST'])
def create_parcel_delivery_order():
    """
    register new parcel delivery order
    """
    current_user = get_jwt_identity()
    # if current_user['admin'] == True:
    #     return jsonify({'message':'Access rights to this route denied', 'status': 'Failure'}), 403

    data = request.get_json(force=True)

    if not data:
        return jsonify({'message': 'Cannot create parcel, some fields are missing', "status": "Failure"}), 400

    if (len(data.keys()) != 4):
        return jsonify({'message': 'Cannot create parcel due to missing fields', "status": "Failure"}), 400

    pickup_location = data['pickup_location']
    recipient = data['recipient']
    destination = data['destination']
    description = data['description']

    if len(description) < 5:
        return jsonify({'message': 'Please provide an elaborate parcel description', "status": "Failure"}), 400

    ParcelOrder().post_new_order(
        pickup_location, destination, recipient, description)

    return jsonify({'message': 'Parcel order successfully created', "status": "Success"}), 201


@app.route('/api/v1/parcels', methods=['GET'])
@jwt_required
def get_all_orders():
    current_user = get_jwt_identity()
    if current_user['admin'] != True:
        return jsonify({'message':'Access rights to this route denied', 'status': 'Failure'}), 403

    if ParcelOrder().get_all_parcels():
        return jsonify({"Status": "Success", 'response': ParcelOrder.get_all_parcels()}), 200
    return jsonify({'message': 'No parcels have been added', "Status": "Failure"}), 404

# get one parcel delivery order


@app.route('/api/v1/parcels/<int:parcelId>', methods=['GET'])
@jwt_required
def get_one_delivery_order(parcelId):
    """ get parcel by parcelId """
    logged_in_user = get_jwt_identity()
    parcel = ParcelOrder().get_one_parcel(parcelId)
    if parcel:
        return jsonify(parcel), 200
    return jsonify({'message': 'Cannot find parcel with that Id!', 'Status': 'Failure'}), 400


@app.route('/api/v1/parcels/<int:parcelId>/status', methods=['PUT'])
@jwt_required
def update_status(parcelId):
    """
    updated the status of a parcel delivery order
    """
    current_user = get_jwt_identity()
    if current_user['admin'] != True:
        return jsonify({'message':'Access to this route denied!', 'status':'Failure'}), 403
    data = request.get_json()
    status = data.get("status")
    parcel = ParcelOrder().update_parcel_order_status(parcelId, status)
    if not parcel['parcelId']:
        return jsonify({"message": "No parcel exists under that Id", "status": "Failure"}), 400

    return jsonify({"message": "Parcel status succesfully Updated", "status": "Success", "response": "Parcel Order status updated"}), 200
    

@app.route('/api/v1/parcels/<int:parcelId>/destination', methods= ['PUT'])
@jwt_required
def update_destination(parcelId):
    """
    Update the destination of a parcel delivery order
    """
    current_user = get_jwt_identity()
    if current_user['admin'] == True:
        return jsonify({'message':'Access to this route denied!', 'status':'Failure'}), 403
    data = request.get_json()
    destination = data.get("destination")
    parcel = ParcelOrder().update_parcel_order_destination(parcelId, destination)
    if not parcel['parcelId']:
        return jsonify({"message": "No parcel exists under that Id", "Status": "Failure"}), 400

    return jsonify({"message": "Parcel destination succesfully Updated", "destination": "Success", "response": "Parcel Order destination updated"}), 200
    


@app.route('/api/v1/parcels/<int:parcelId>/location', methods= ['PUT'])
def update_the_current_location(parcelId):
    current_user = get_jwt_identity()
    if current_user['admin'] == True:
        return jsonify({'message':'Access to this route denied!', 'status':'Failure'}), 403
    data = request.get_json()
    pickup_location = data.get("pickup_location")
    parcel = ParcelOrder().update_parcel_order_pickup_location(parcelId, pickup_location)
    if not parcel['parcelId']:
        return jsonify({"message": "No parcel exists under that Id", "pickup_location": "Failure"}), 400

    return jsonify({"message": "Parcel pickup_location succesfully Updated", "status": "Success", "response": "Parcel Order pickup_location updated"}), 200
    