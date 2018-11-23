from sendit.database import Database



class ParcelOrder:
    """ parcel class that creates a parcel for only a user that is registered """

    def __init__(self, recipient, pickup_location, destination, description):
        self.recipient = recipient
        self.pickup_location = pickup_location
        self.destination = destination
        self.description = description

    db = Database()
    db.create_tables()

    def post_new_order(self, pickup_location, destination, recipient, description):
        post_query = "INSERT INTO parcels (pickup_location, destination, recipient, description) \
        VALUES ('{}', '{}', '{}', '{}')".format(pickup_location, destination, recipient, description)
        self.cursor.execute(post_query)

    def get_all_parcels(self):
        get_parcels_query= "SELECT * FROM parcels"
        self.cursor.execute(get_parcels_query)
        return self.cursor.fetchall()

    def get_one_parcel(self,parcelId):
        get_one_parcel_query= "SELECT * FROM parcels WHERE parcelId= '{}' ".format(parcelId)
        self.cursor.execute(get_one_parcel_query)        
        return self.cursor.fetchone()

    def update_parcel_order_status(self, parcelId, status):
        """
        update parcel order status
        """
        update_status_query= "UPDATE parcels SET status = '{}' WHERE parcelId = '{}' ".format (status, parcelId)
        self.cursor.execute(update_status_query)

    def update_parcel_destination(self, parcelId):
        """update parcel order destination"""
        update_destination_query= "UPDATE parcels SET destination = '{}' WHERE parcelId= '{}' ".format(destination, parcelId)
        self.cursor.execute(update_destination_query)

    def update_present_location(self,parcelId):
        """
        Update the present location of a parcel order
        """
        update_location= "UPDATE parcels SET present_location = '{}' WHERE parcelId= '{}' ".format(destination, parcelId)
        self.cursor.execute(update_location)
