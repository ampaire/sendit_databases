from . import main
from flask import request, jsonify

def app_error(message, code):
    if request.accept_mimetypes.accept_json and not request.accept_mimetypes.accept_html:
        response = jsonify{'message':'error'}
        response.status_code = code
        return response
    else:
        return message, code


@main.app_errorhandler(404)
def page_not_known(e):
    """urls not found"""
    return app_error('Page not found', 404)


@main.app_errorhandler(500)
def internal_server_error(e):
    """Internal server errors"""
    return app_error('Internal Server Error', 500)