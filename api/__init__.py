"""
Module API Create Blueprint API
"""

from flask import Blueprint
from flask_restx import Api

from .product import ns as product_ns
from .user import ns as user_ns

blue_print = Blueprint("api_blueprint", __name__)
api = Api(
    blue_print,
    title="gym_equipment_api",
    version="1.0",
    description="gym_equipment_api",
    # ui=True,
)

api.add_namespace(product_ns, path="/p")
api.add_namespace(user_ns, path="/u")