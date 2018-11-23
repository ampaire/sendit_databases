from flask import Flask
from sendit import app
@app.route('/')
def index():
    return 'Welcome to sendIt. Happy browsing'
