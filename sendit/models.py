from werkzeug.security import generate_password_hash, check_password_hash
class User:
    """class to create the users"""
    def __init__(self,userid, username, email, password,role):
        self.userid = userid
        self.username = username
        self.email = email
        self.password_hash = self.create_a_password_for_a_user(password)
        self.role = role

    @staticmethod
    def create_a_password_for_a_user(password):
        return generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

class ParcelOrder:
    """ parcel class that creates a parcel for only a user that is registered """

    def __init__(self, recipient, pickup_location, destination, description):
        self.recipient = recipient
        self.pickup_location = pickup_location
        self.destination = destination
        self.description = description
    

