import os
import time
import datetime
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash


class Database:
    """
       Class for working on the users logic
    """

    def __init__(self):
        try:
            self.connection = psycopg2.connect(dbname='sendit',
                                                user='postgres',
                                                password='akankunda',
                                                host='localhost',
                                                port='5432')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print('we are good')
        except(Exception, psycopg2.DatabaseError) as error:
            raise error

    def create_tables(self):
        commands = (
            """
            CREATE TABLE IF NOT EXISTS "useers" (
                    userId SERIAL PRIMARY KEY,
                    username VARCHAR(50) NOT NULL,
                    email VARCHAR(50) NOT NULL,
                    password VARCHAR(200) NOT NULL,
                    role VARCHAR (15) NOT NULL

                )
            """,
            """
            CREATE TABLE IF NOT EXISTS "parscels" (                    
                    parcelId SERIAL PRIMARY KEY,
                    userId INT REFERENCES users(userId),
                    username VARCHAR(30) NOT NULL,
                    pickup_location VARCHAR(30) NOT NULL,
                    recipient VARCHAR(30) NOT NULL,
                    description VARCHAR(100) NOT NULL,
                    status VARCHAR(15) NOT NULL,
                    parcel_created date
                )
                """,)
        for command in commands:
            self.cursor.execute(command)

    def register_user(self,userId, username, email, password,role):
        query = "INSERT INTO users (userId, username, email, password, role) \
        VALUES ('{}', '{}', '{}', '{}', '{}')".format(userId, username, email, password,role)
        self.cursor.execute(query)



