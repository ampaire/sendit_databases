import json
import unittest
from sendit.api.routes import register_new_user, login, get_all_users
from sendit import app
from sendit.database import Database


class TestUserRoutes(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client(self)
        self.client.testing = True
        db = Database
        # db.create_tables()
        # db.drop_tables()
    
    demo_user = {
        'username': 'Effie',
        'password': 'password',
        'email': 'Effie@mail.com'
    }

    new_user = {
        'username': 'phem',
        'password': 'password2',
        'email': 'phem@mail.com'
    }

    missing_email_in_new_user = {
        'username': 'correctuser',
        'password': 'wrongpassword'
    }

    short_password_in_new_user = {
        'username': 'phem',
        'password': '12',
        'email': 'phem@mail.com'
    }

    invalid_username_in_new_user = {
        'username': '.Effie',
        'password': 'password',
        'email': 'phem@mail.com'
    }

    invalid_email_in_new_user = {
        'username': 'Effie',
        'password': 'password',
        'email': 'Effie'
    }

    null_user_details = {'username': '', 'password': '', 'email': ''}
    
    invalid_key = {'password':'wrongpassword'}
    
    login_user = {'password': 'password', 'email': 'Effie@mail.com'}

    null_user = {}

    invalid_email_credentials = {
        'password': 'password',
        'email': 'phem@mail.com'
    }

    invalid_email_format_at_login = {'password': 'password', 'email': '.'}

    invalid_password_credentials = {
        'password': 'wrongpassword',
        'email': 'Effie@mail.com'
    }
    missing_password_field = {
        'email': 'Effie@mail.com'
    }

    def test_can_regester_a_user(self):
        response = self.client.post(
            ('api/v1/auth/signup'), data=json.dumps(self.new_user))
        self.assertFalse(response.status_code == 400)

    def test_an_email_already_in_emails(self):
        response = self.client.post(
            ('api/v1/auth/signup'), data=json.dumps(self.test_user))
        self.assertTrue(response.status_code == 400)

    def test_missing_password_field_at_sign_up(self):
        response = self.client.post(
            ('api/v1/auth/signup'),
            data=json.dumps(self.missing_password_field))
        self.assertFalse(response.status_code == 400)

    def test_length_of_the_user_password(self):
        response = self.client.post(
            ('api/v1/auth/signup'),
            data=json.dumps(self.short_password_in_new_user))
        self.assertFalse(response.status_code == 200)

    def test_missing_values_while_signing_up(self):
        response = self.client.post(
            ('api/v1/auth/signup'),
            data=json.dumps(self.null_user_details))
        self.assertFalse(response.status_code == 400)

    def test_cannot_regester_with_missing_strings(self):
        response = self.client.post(
            ('api/v1/auth/signup'),
            data=json.dumps(self.null_user))
        self.assertFalse(response.status_code == 200)

    def test_user_can_login(self):
        response = self.client.post(
            ('api/v1/login'), data=json.dumps(self.login_user))
        self.assertFalse(response.status_code == 200)

    def test_user_enters_wrong_details(self):
        response = self.client.post(
            ('api/v1/login'), data=json.dumps(self.null_user_details))
        self.assertTrue(response.status_code == 404)

    def test_wrong_email_at_login(self):
        response = self.client.post(
            ('api/v1/login'),
            data=json.dumps(self.invalid_email_credentials))
        self.assertFalse(response.status_code == 401)

    def test_wrong_password_at_login(self):
        response = self.client.post(
            ('api/v1/login'),
            data=json.dumps(self.invalid_password_credentials))
        self.assertFalse(response.status_code == 401)

    if __name__ == "main":
        unittest()