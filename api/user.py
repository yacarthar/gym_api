"""
Product Routers
"""

from flask import request, jsonify
from flask_restx import Resource, marshal
from flask_restx.fields import MarshallingError
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from model import user, cart
from api.schema.user import (
    ns,
    input_post_schema,
    input_put_schema,
    output_get_schema,
    input_put_cart_schema,
)
from api.auth import requires_token, requires_api_key
from utils import flatten


@ns.route("/")
class Users(Resource):
    @requires_api_key
    @ns.expect(input_post_schema, validate=True)
    def post(self):
        """create users"""
        # try:
        data = marshal(ns.payload, input_post_schema, skip_none=True)
        _user = user.find_one({"sub": data["sub"]})
        if _user:
            return {"message": "user exists"}, 409
        else:
            res = user.insert_one(data)
            return {"created_user": str(res.inserted_id)}, 200
        # except Exception as e:
        #     return {"error": str(e)}, 400


@ns.route("/id/<user_id>")
class User(Resource):
    def get(self, user_id):
        """get user by id"""
        try:
            _user = user.find_one({"_id": ObjectId(user_id)}, projection={"_id": False})
            if _user:
                return marshal(_user, output_get_schema, skip_none=True), 200
            else:
                return {"error": "user not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 400


@ns.route("/sub/")
class User(Resource):
    @requires_token
    def get(self, user_sub):
        """get user by sub"""
        print(user_sub)
        try:
            _user = user.find_one({"sub": user_sub}, projection={"_id": False})
            if _user:
                return marshal(_user, output_get_schema, skip_none=True), 200
            else:
                return {"error": "user not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    @requires_token
    @ns.expect(input_put_schema, validate=True)
    def put(self, user_sub):
        """update users"""
        try:
            data = marshal(ns.payload, input_put_schema, skip_none=True)
            if "sub" in data:
                data.pop("sub")
            data = flatten(data)
            print(data)
        except MarshallingError as e:
            return {"error": str(e)}, 400
        try:
            res = user.find_one_and_update(
                {"sub": user_sub},
                {"$set": data},
                projection={"_id": False},
                return_document=ReturnDocument.AFTER,
            )
            return res, 200
        except Exception as e:
            return {"error": str(e)}, 400


@ns.route("/cart/")
class Cart(Resource):
    @requires_token
    @ns.expect(input_put_cart_schema, validate=True)
    def put(self, user_sub):
        """update one item to cart or create cart"""
        print(user_sub)
        try:
            data = marshal(ns.payload, input_put_cart_schema, skip_none=True)
            cart.update_one(
                {"user_sub": user_sub}, {"$set": {"items": data["items"]}}, upsert=True
            )
            return 200
        except Exception as e:
            return {"error": str(e)}, 400

    @requires_token
    def get(self, user_sub):
        """get cart"""
        print(user_sub)
        try:
            _cart = cart.find_one({"user_sub": user_sub}, projection={"_id": False})
            if _cart:
                return _cart["items"], 200
            else:
                return {"error": "cart not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 400
