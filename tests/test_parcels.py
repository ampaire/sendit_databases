import unittest
from sendit import app
from sendit.database import Database
from sendit.models.user_models import User
from sendit.models.parcel_models import ParcelOrder
from flask import Flask, url_for, request, json


class TestparcelRoutes(unittest.TestCase):
    """Tests to check the validity of the parcels routes"""
    # Tests for adding a parcel delivery order

    def setUp(self):
        self.client = app.test_client(self)
        self.client.testing = True
        self.signup = {'username': 'Effie',
                       'email': 'effie22@gmail.com', 'password': 'effie'}
        self.login = {'email': 'effie@gmail.com', 'password': 'effie'}
        self.parcel_update = {"present_location": "Kabale"}
        self.null_user_fields = {'username': '', 'password': '', 'email': ''}
        self.new_parcel = {'pickup_loction': 'Lubaga',
                           'destination': 'Nsyambya',
                           'recipient': '0777777777',
                           'description': 'A large size tray of 2kgs'
                           }

        db = Database()
        db.create_tables()

    def tearDown(self):
        db = Database()
        db.drop_tables
        """
        First login a user to get the Access token
        """

    def create_token(self):
        response = self.client.post('/api/v1/auth/login',
                                   data=json.dumps(
                                       self.login),
                                   content_type='application/json')
        data = json.loads(response.data.decode())
        return 'Bearer ' + data['Access_token']

    def test_signup(self):
        response = self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                                    content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_signin(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login),
                                      content_type='application/json')
                                      
        self.assertEqual(login_data.status_code, 200)

    def test_parcel_delivery_order_added(self):
        token = None
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.post('/api/v1/parcels', data=json.dumps(self.new_parcel), content_type='application/json',
            headers={'Authorization':self.create_token()})

        self.assertFalse(response.status_code == 400)

    def test_missing_fields_at_adding_a_parcel_delivery_order(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.post(
            '/api/v1/parcels',
            data=json.dumps(self.null_user_fields),
            headers={'Authorization': self.create_token()})
        self.assertFalse(response.status_code == 200)

    def test_empty_fields_at_adding_a_parcel_delivery_order(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.post(
            '/api/v1/parcels',
            headers={'Authorization': self.create_token()})
        self.assertFalse(response.status_code == 200)

    def test_unauthorized_user_at_adding_a_parcel_delivery_order(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.post(
            '/api/v1/parcels',
            data=json.dumps(self.new_parcel))
        self.assertFalse(response.status_code == 200)

     # Tests get of a single parcel
    def test_getting_a_parcel(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.get(
            '/api/v1/parcels/2',
        headers={'Authorization': self.create_token()})
        self.assertFalse(response.status_code == 400)

    def test_unauthorized_user_at_getting_a_parcel(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.get('/api/v1/parcels/2')
        self.assertTrue(response.status_code == 401)

    def test_unknown_parcel_at_getting_a_parcel(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.get(
            '/api/v1/parcels/ll',
        headers={'Authorization': self.create_token()})
        self.assertFalse(response.status_code == 200)

    # Tests get of a parcel by name
    def test_getting_a_parcel_by_name(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.get(
            '/api/v1/parcels/1' ,
        headers={'Authorization': self.create_token()})
        self.assertFalse(response.status_code == 400)

    def test_unauthorized_user_at_getting_a_parcel_by_name(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.get(
            '/api/v1/parcels/1' )
        self.assertTrue(response.status_code == 401)


    def test_update_parcel(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.put(
            '/api/v1/parcels/2/location',
            data=json.dumps(self.parcel_update),
        headers={'Authorization': self.create_token()})
        self.assertTrue(response.status_code == 200)

    def test_update_parcel(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.put(
            '/api/v1/parcels/2/status',
            data=json.dumps(self.parcel_update),
        headers={'Authorization': self.create_token()})
        self.assertFalse(response.status_code == 400)

    def test_unauthorized_user_at_update_parcel(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.put(
            '/api/v1/parcels/2',
            data=json.dumps(self.parcel_update))
        self.assertFalse(response.status_code == 200)

    def test_no_data_at_update_parcel(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.put(
            '/api/v1/parcels/2',
        headers={'Authorization': self.create_token()})
        self.assertFalse(response.status_code == 200)

    def test_wrong_parcel_id_at_update_parcel(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.put(
            '/api/v1/parcels/2',
            data=json.dumps(self.parcel_update),
        headers={'Authorization': self.create_token()})
        self.assertFalse(response.status_code == 200)


    # Tests for getting all parcels
    def test_getting_all_parcels(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.get(
            '/api/v1/parcels',
        headers={'Authorization': self.create_token()})
        self.assertFalse(response.status_code == 400)

    def test_unauthorized_user_at_getting_all_parcels(self):
        self.client.post('/api/v1/auth/signup', data=json.dumps(self.signup),
                         content_type='application/json')
        login_data = self.client.post('/api/v1/auth/login', data=json.dumps(self.login), 
                            content_type='application/json')
        Access_token = json.loads(login_data.data.decode())
        response = self.client.get('/api/v1/parcels/1')
        self.assertTrue(response.status_code == 401)

    if __name__ == "main":
        unittest()
