from flask_restx import Namespace, fields
from bson.objectid import ObjectId


class ObjectID(fields.String):
    def format(self, value):
        return ObjectId(value)


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
        # "fav": ObjectID()
    },
)