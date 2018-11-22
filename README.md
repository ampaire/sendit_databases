## Project Title

SendIT
[![Build Status](https://travis-ci.org/ampaire/sendit_databases.svg?branch=feature)](https://travis-ci.org/ampaire/sendit_databases)
[![Coverage Status](https://coveralls.io/repos/github/ampaire/sendit_databases/badge.svg)](https://coveralls.io/github/ampaire/sendit_databases)
[![Maintainability](https://api.codeclimate.com/v1/badges/e45ee7961a5399f8b081/maintainability)](https://codeclimate.com/github/ampaire/sendit_api/maintainability)
## github repo link
https://github.com/ampaire/sendit_databases

## Description
SendIT is an online courrier service that enables users to send and receive parcel delivery orders
SendIT product enables users to:-
*  create an account and login
*  create parcel delivery orders
*  view their parcel delivery orders
*  view number of parcels they have created
*  Change the destination of a delivery order

SendIT also has the provision of allowing the admin to
*  update the status of a delivery order
* update the present location of a parcel delivery order

### Prerequisites
 * Postman
 * Virtual environment
 * pytest
 * pytest--cov
 * pylint
 * python
 * flask frame work
 * gunicorn
 * coveralls
 * coverage
 * postgres
 * flask-jwt-

##
| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| POST | /api/v1/auth/login | Logs in a user to the application|
| GET | api/v1/auth/USERS | Gets all users that have signed up to the application |
| POST | api/v1/auth/register | Add a new user to the application |
| GET | api/v1/parcels | Retrieves all parcel orders|
| POST | api/v1/parcels | Creates a new parcel order |
| GET | api/v1/parcels/&lt;parcelId&gt; | Get a parcel order by id |
| PUT | api/v1/parcels/&lt;parcelId&gt;/cancel | Updates the status of a specific parcel order  |
| PUT | api/v1/parcels/&lt;parcelId&gt;/pickup_location | Updates the pickup_location of a parcel delivery order |
| PUT | ap1/v1/parcels/&lt;parcelId&gt;/destination | Updates the destination of a parcel delivery order|

## BUILT WITH

* Flask - Python Framework used
* Postgresql
* flask-jwt-extended

## SETTING UP APPLICATION

1. Create a folder sendit_databases and clone repository to the folder

    **```git clone https://github.com/ampaire/sendit_databases.git```**

2. Create a virtual environment that you are going to use while running the application locally

    **```$ virtualenv venv```**

    **```$ source venv/bin/activate```**

**NB: [More Information on setting up Virtual environments here](https://packaging.python.org/guides/installing-using-pip-and-virtualenv/)**

3. Install all project dependencies using

    **```pip3 install -r requirements.txt```**

4. Set up a secret key for security purposes of your application

    **```SECRET_KEY = '<your_secret_key>'```**

## RUNNING APPLICATION

1.  To launch the application, run the following command in your terminal

    **```python run.py```**


2. To run tests on the application, run the following command in your terminal

    **```pytest -v```**



### Tools Used

* [PIP](https://pip.pypa.io/en/stable/) - Python package installer.
* [Flask](http://flask.pocoo.org/) - Web microframework for Python.
* [Virtual Environment](https://virtualenv.pypa.io/en/stable/) - Used to create isolated Python environments
* [PostgreSQL](https://www.postgresql.org/docs/)- getting started with postgres
* [SQL in 24 hours](http://www.allitebooks.com/sql-in-24-hours-sams-teach-yourself-6th-edition/)- Get you started with SQL querries



### Acknowledgements
My sincere acknowledgements to Andela Uganda Bootcamp 14 team for the advise and encouragement
## Authors

Ampaire Phemia