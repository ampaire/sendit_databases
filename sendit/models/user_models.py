from flask import Flask
from sendit import app
from sendit.database import Database
from werkzeug.security import generate_password_hash, check_password_hash

db_class = Database()

class User:
    """class to create the users"""

    @staticmethod
    def create_a_password_for_a_user(password):
        return generate_password_hash(password)

    @staticmethod
    def verify_password(password):
        return check_password_hash(db_class.password_hash, password)

    @staticmethod
    def define_admin_rights():
        admin = "UPDATE users SET user = True WHERE userId == 1;"
        db_class.cursor.execute(admin)

    @staticmethod    
    def post_user(username, email, password):
        signup_query = "INSERT INTO users ( username, email, password) \
        VALUES ('{}', '{}', '{}')".format(username, email, password)
        db_class.cursor.execute(signup_query)

    @staticmethod
    def get_user_by_email(email):
        query = "SELECT email FROM users WHERE email= '{}'".format(email)
        db_class.cursor.execute(query)
        user = db_class.cursor.fetchone()
        return user

    @staticmethod
    def get_users():
        query = "SELECT username FROM users"
        db_class.cursor.execute(query)
        users = db_class.cursor.fetchall()
        return users 

    @staticmethod
    def get_logged_in_user(email, password):
        login_query = "SELECT email FROM users WHERE email ='{}'".format(
            email)
        db_class.cursor.execute(login_query)
        return [email, password]

    @staticmethod
    def get_all_availabe_users(username, email):
        getUsers_query = "SELECT (username,email) FROM user WHERE email = \
        '{}' and username = '{}'".format(email, password)
        db_class.cursor.execute(getUsers_query)