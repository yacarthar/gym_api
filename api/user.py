"""
Product Routers
"""

from flask import request, jsonify
from flask_restx import Resource, marshal
from flask_restx.fields import MarshallingError
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from model import user
from api.schema.user import ns, input_post_schema, input_put_schema, output_get_schema
from utils import flatten

@ns.route("/")
class Users(Resource):
    @ns.expect(input_post_schema, validate=True)
    def post(self):
        """create users"""
        data = marshal(ns.payload, input_post_schema, skip_none=True)
        try:
            _user = user.find_one({"sub": data["sub"]})
            if _user:
                return {"message": "user exists"}, 409
            else:
                res = user.insert_one(data)
                return {"created_user": str(res.inserted_id)}, 200
        except Exception as e:
            return {"error": str(e)}, 400


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


@ns.route("/sub/<user_sub>")
class User(Resource):
    def get(self, user_sub):
        """get user by sub"""
        try:
            _user = user.find_one({"sub": user_sub}, projection={"_id": False})
            if _user:
                return marshal(_user, output_get_schema, skip_none=True), 200
            else:
                return {"error": "user not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    @ns.expect(input_put_schema, validate=True)
    def put(self, user_sub):
        """create users"""
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
