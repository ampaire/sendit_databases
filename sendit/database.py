import os
import time
import datetime
import psycopg2
from sendit.models import User
from werkzeug.security import generate_password_hash, check_password_hash


class Database:
    def __init__(self):
        try:
            if(os.getenv("FLASK_ENV")) == "Production":
                self.connection = psycopg2.connect(os.getenv("DATABASE_URL"))
            self.connection = psycopg2.connect(dbname='sendit',
                                               user='postgres',
                                               password='akankunda',
                                               host='localhost',
                                               port='5432')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()

        except(Exception, psycopg2.DatabaseError) as error:
            raise error

    def drop_tables(self):
        self.cursor.execute("DROP TABLE IF EXISTS users, parcels CASCADE")

    def create_tables(self):
        parcel_orderss = (
            """
            CREATE TABLE IF NOT EXISTS "users" (
                    userId SERIAL PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(50) NOT NULL,
                    password VARCHAR(200) NOT NULL,
                    role BOOLEAN DEFAULT False,
                    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP


                )
            """,
            """
            CREATE TABLE IF NOT EXISTS "parcels" (                    
                    parcelId SERIAL PRIMARY KEY,
                    userId INT REFERENCES users(userId) NULL,
                    username VARCHAR(30) NULL,
                    pickup_location VARCHAR(30) NOT NULL,
                    present_location VARCHAR(30) NULL,
                    recipient VARCHAR(30) NOT NULL,
                    destination VARCHAR(30) NOT NULL,
                    description VARCHAR(100) NOT NULL,
                    status VARCHAR(15) NULL,
                    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,)
        for parcel_orders in parcel_orderss:
            self.cursor.execute(parcel_orders)

    # metthods for the users
    def get_user(self, username, email, password):
        signup_query = "INSERT INTO users ( username, email, password) \
        VALUES ('{}', '{}', '{}')".format(username, email, password)
        self.cursor.execute(signup_query)

    def get_logged_in_user(self, email, password):
        login_query = "SELECT email FROM users WHERE email ='{}'".format(
            email)
        self.cursor.execute(login_query)
        return [email, password]

    def get_all_availabe_users(self, username, email):
        getUsers_query = "SELECT (username,email) FROM user WHERE email = \
        '{}' and username = '{}'".format(email, password)
        self.cursor.execute(getUsers_query)

    # methods for the parcels
    def post_new_order(self, pickup_location, destination, recipient, description):
        post_query = "INSERT INTO parcels (pickup_location, destination, recipient, description) \
        VALUES ('{}', '{}', '{}', '{}')".format(pickup_location, destination, recipient, description)
        self.cursor.execute(post_query)

    def get_all_parcels(self, username, pickup_location, destination, recipient, description, status):
        get_parcels_query= "SELECT * FROM parcels"
        self.cursor.execute(get_parcels_query)

    def get_one_parcel(self, username, pickup_location, destination, recipient, description, status):
        get_one_parcel_query= "SELECT * FROM parcels WHERE parcelId= {}".format(parcelId)
        self.cursor.execute(get_one_parcel_query)


    def update_parcel_order_status(self, status):
        """
        update parcel order status
        """
        status_query= "SELECT parcelId FROM parcels WHERE parcelId= {}".format(parcelId)
        self.cursor.execute(status_query)

        update_status_query= "UPDATE parcels SET status = {},\
        date_updated = CURRENT_TIMESTAMP WHERE parcelId = {}".format (status, parcelId)
        self.cur.execute(update_status_query)

    def update_parcel_destination(self, destination):
        """update parcel order destination"""
        destination_query= "SELECT parcelId FROM parcels WHERE parcelId= {}".format(parcelId)
        self.cursor.execute(status_query)

        update_destination_query= "UPDATE parcels SET destination = {},\
        date_updated= CURRENT_TIMESTAMP WHERE parcelId= {}".format(destination, parcelId)
        self.cursor.execute(update_destination_query)

    def update_present_location(self,present_location):
        """
        Update the present location of a parcel order
        """
        status_query= "SELECT parcelId FROM parcels WHERE parcelId= {}".format(parcelId)
        self.cursor.execute(status_query)

        update_location= "UPDATE parcels SET present_location={},\
        date_updated= CURRENT_TIMESTAMP WHERE parcelId= {}".format(present_location, parcelId)"
