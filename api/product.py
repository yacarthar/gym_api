"""
Product Routers
"""

from flask import request, jsonify
from flask_restx import Resource, Namespace
from bson.objectid import ObjectId
from model import product

ns = Namespace("Product", description="Product operations")
@ns.route("/")
class Products(Resource):
    def get(self):
        """list products"""
        items = product.find(
            {},
            projection={"_id": False}
        )
        return list(items)

@ns.route("/<identifier>")
class Product(Resource):
    def get(self, identifier):
        """get one product"""
        query_by = request.args.get("query_by")
        if query_by == "object_id":
            return product.find_one(
                {"_id": ObjectId(identifier)},
                projection={"_id": False}
            )
        elif query_by == "short_id":
            return product.find_one(
                {"id": identifier},
                projection={"_id": False}
            )
        elif query_by == "name":
            return product.find_one(
                {"name": identifier},
                projection={"_id": False}
            )
        else:
            return {"message": "Bad Request: missing parameter query_by"}, 400
