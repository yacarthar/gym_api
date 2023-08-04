"""
Product Routers
"""

from flask import request, jsonify
from flask_restx import Resource, Namespace, fields, marshal
from bson.objectid import ObjectId
from model import user

ns = Namespace("User", description="User operations")
user_schema = ns.model(
    "user",
    {
        "sub": fields.String(required=True),
        "address": fields.Nested(
            ns.model(
                "address",
                {
                    "country": fields.String(),
                    "city": fields.String(),
                    "street": fields.String(),
                    # "lat-long": fields.String(),
                },
            ),
            skip_none=True,
        ),
        "dob": fields.DateTime(),
        "card": fields.Nested(
            ns.model(
                "card",
                {
                    "brand": fields.String(enum=["VISA", "MasterCard"]),
                    "pan": fields.String(pattern=r"[\d]{16}", max_length=16),  # primary account number
                    "expiration": fields.Nested(
                        ns.model(
                            "expire",
                            {
                                "year": fields.Integer(min=1900, max=2100),
                                "month": fields.Integer(min=1, max=12),
                            },
                        ),
                        skip_none=True,
                    ),
                    "cvv": fields.String(pattern=r"[\d]{3}", max_length=3),
                },
            ),
            skip_none=True,
        ),
    },
)


@ns.route("/")
class Users(Resource):
    @ns.expect(user_schema, validate=True)
    def post(self):
        """
        create users
        """
        res = marshal(ns.payload, user_schema)
        # res = user.insert_one(ns.payload)
        # return str(res.inserted_id)
        return jsonify(res)


@ns.route("/<user_id>")
class User(Resource):
    def get(self, user_id):
        """get one user"""
        return user.find_one({"name": "jones"}, projection={"_id": False})
