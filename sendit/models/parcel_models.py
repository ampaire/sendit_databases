from sendit.database import Database

db_class = Database()

class ParcelOrder:
    """ parcel class that creates a parcel for only a user that is registered """

   
    @staticmethod
    def post_new_order(pickup_location, destination, recipient, description):
        post_query = "INSERT INTO parcels (pickup_location, destination, recipient, description) \
        VALUES ('{}', '{}', '{}', '{}')".format(pickup_location, destination, recipient, description)
        db_class.cursor.execute(post_query)

    @staticmethod
    def get_all_parcels(self):
        get_parcels_query= "SELECT * FROM parcels"
        db_class.cursor.execute(get_parcels_query)
        return db_class.cursor.fetchall()

    @staticmethod
    def get_one_parcel(parcelId):
        get_one_parcel_query= "SELECT * FROM parcels WHERE parcelId= '{}' ".format(parcelId)
        db_class.cursor.execute(get_one_parcel_query)        
        return db_class.cursor.fetchone()

    @staticmethod
    def update_parcel_order_status(parcelId, status):
        """
        update parcel order status
        """
        update_status_query= "UPDATE parcels SET status = '{}' WHERE parcelId = '{}' ".format (status, parcelId)
        db_class.cursor.execute(update_status_query)

    @staticmethod
    def update_parcel_destination(parcelId):
        """update parcel order destination"""
        update_destination_query= "UPDATE parcels SET destination = '{}' WHERE parcelId= '{}' ".format(destination, parcelId)
        db_class.cursor.execute(update_destination_query)

    @staticmethod
    def update_present_location(parcelId):
        """
        Update the present location of a parcel order
        """
        update_location= "UPDATE parcels SET present_location = '{}' WHERE parcelId= '{}' ".format(destination, parcelId)
        db_class.cursor.execute(update_location)
