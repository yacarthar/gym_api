"""
Product Routers
"""

from flask import request, jsonify
from flask_restx import Resource, marshal
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from model import user
from api.schema.user import ns, user_schema


@ns.route("/")
class Users(Resource):
    @ns.expect(user_schema, validate=True)
    def post(self):
        """create users"""
        data = marshal(ns.payload, user_schema, skip_none=True)
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
                return marshal(_user, user_schema, skip_none=True), 200
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
                return marshal(_user, user_schema, skip_none=True), 200
            else:
                return {"error": "user not found"}, 404
        except Exception as e:
            return {"error": str(e)}, 400

    @ns.expect(user_schema, validate=True)
    def put(self, user_sub):
        """create users"""
        data = marshal(ns.payload, user_schema, skip_none=True)
        try:
            res = user.find_one_and_update(
                {"sub": user_sub},
                {"$set": data},
                projection={"_id": False},
                return_document=ReturnDocument.AFTER,
            )
            print(res)
            return res, 200
        except Exception as e:
            return {"error": str(e)}, 400
