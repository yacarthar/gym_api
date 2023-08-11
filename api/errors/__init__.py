from flask import jsonify
from .custom_errors import Error

def error_handler(e):
    response = jsonify(e.error)
    response.status_code = e.status_code
    return response