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
                    role VARCHAR(50) DEFAULT 'user',
                    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP


                )
            """,
            """
            CREATE TABLE IF NOT EXISTS "parcels" (                    
                    parcelId SERIAL PRIMARY KEY,
                    userId integer,
                    FOREIGN KEY (userId)
                    REFERENCES users(userId),
                    username VARCHAR(20),
                    FOREIGN KEY (username)
                    REFERENCES users(username),
                    pickup_location VARCHAR(30) NOT NULL,
                    present_location VARCHAR(30) DEFAULT 'unknown',
                    recipient VARCHAR(30) NOT NULL,
                    destination VARCHAR(30) NOT NULL,
                    description VARCHAR(100) NOT NULL,
                    status VARCHAR(15) DEFAULT 'Pending',
                    created_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_on TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """,)
        for parcel_orders in parcel_orderss:
            self.cursor.execute(parcel_orders)

    # metthods for the users
    def define_admin_rights(self):
        admin = "INSERT INTO users(email, username, password, role)\ VALUES('admin@sendit.com', 'admin', 'admin', 'admin')"
        self.cursor.execute(admin)
        
    def get_user(self, username, email, password):
        signup_query = "INSERT INTO users ( username, email, password) \
        VALUES ('{}', '{}', '{}')".format(username, email, password)
        self.cursor.execute(signup_query)

    def get_user_by_email(self, email):
        query = "SELECT email FROM users WHERE email= '{}'".format(email)
        self.cursor.execute(query)
        user = self.cursor.fetchone()
        return user

    def get_users(self):
        query = "SELECT username FROM users"
        self.cursor.execute(query)
        users = self.cursor.fetchall()
        return users        

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
