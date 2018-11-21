import os
import time
import datetime
import psycopg2
from app.models import User
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
                    role BOOLEAN DEFAULT False
                    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,


                )
            """,
            """
            CREATE TABLE IF NOT EXISTS "parcels" (                    
                    parcelId SERIAL PRIMARY KEY,
                    userId INT REFERENCES users(userId),
                    username VARCHAR(30),
                    pickup_location VARCHAR(30) NOT NULL,
                    present_location VARCHAR(30) NOT NULL,
                    recipient VARCHAR(30) NOT NULL,
                    destination VARCHAR(30) NOT NULL,
                    description VARCHAR(100) NOT NULL,
                    status VARCHAR(15) ,
                    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                )
                """,)
        for parcel_orders in parcel_orderss:
            self.cursor.execute(parcel_orders)

    # metthods for the users
    def register_user(self, username, email, password):
        signup_query = "INSERT INTO users ( username, email, password) \
        VALUES ('{}', '{}', '{}')".format(username, email, password)
        # if signup_query:
        #     return jsonify({"message": "User with same credentials already exists! Try logging in"}, {"status": "Failure"})
        self.cursor.execute(signup_query)

    def login_a_user(self, email, password):
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

    # def get_all_parcels(self, username, pickup_location, destination, recipient, description):
    #     get_parcels_query


    def update_parcel_order(self, myorder):
            """update parcel data"""
            try:
                self.cur.execute(
                    "UPDATE parcels SET destination='{}', pickupLocation={}, destination = '{}',\
                    recipient = '{}', status = '{}',\
                    date_updated = CURRENT_TIMESTAMP WHERE orderID = {}".format(myorder.destination,\
                    myorder.pickupLocation, myorder.destination, myorder.recipient, myorder.status, myorder.orderID)
                )

            except:
                return False