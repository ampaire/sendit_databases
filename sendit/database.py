import os
import time
import datetime
import psycopg2
from psycopg2.extras import RealDictCursor


class Database:
    def __init__(self):
        try:
        
            self.connection = psycopg2.connect(dbname='sendit',
                                               user='postgres',
                                               password='akankunda',
                                               host='localhost',
                                               port='5432')
            self.connection.autocommit = True
            self.cursor = self.connection.cursor(cursor_factory=RealDictCursor)
            
        

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
                    admin BOOLEAN DEFAULT False,
                    creation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    update_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP


                )
            """,
            """
            CREATE TABLE IF NOT EXISTS "parcels" (                    
                    parcelId SERIAL PRIMARY KEY,
                    userId integer,
                    FOREIGN KEY (userId)
                    REFERENCES users (userId),
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
