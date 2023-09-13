from flask_restx import Namespace, fields
from bson.objectid import ObjectId


class ObjectID(fields.String):
    def format(self, value):
        return ObjectId(value)


ns = Namespace("User", description="User operations")


def create_user_schema(require_sub):
    return ns.model(
        "user",
        {
            "sub": fields.String(required=require_sub),
            "address": fields.Nested(
                ns.model(
                    "address",
                    {
                        "country": fields.String(),
                        "city": fields.String(),
                        "district": fields.String(),
                        "ward": fields.String(),
                        "street": fields.String(),
                    },
                ),
                skip_none=True,
            ),
            "gender": fields.String(enum=["Male", "Female"]),
            "phone_number": fields.String(pattern=r"[\d]{10}", max_length=10),
            "dob": fields.Date(),
            "card": fields.Nested(
                ns.model(
                    "card",
                    {
                        "brand": fields.String(enum=["VISA", "MasterCard"]),
                        "pan": fields.String(
                            pattern=r"[\d]{16}", max_length=16
                        ),  # primary account number
                        "expiration": fields.Date(),  # min, max, exclusiveMin and exclusiveMax
                        "cvv": fields.String(pattern=r"[\d]{3}", max_length=3),
                    },
                ),
                skip_none=True,
            ),
            # "fav": ObjectID()
        },
    )


input_post_schema = create_user_schema(require_sub=True)
output_get_schema = create_user_schema(require_sub=True)
input_put_schema = create_user_schema(require_sub=False)

input_put_cart_schema = ns.model(
    "cart",
    {
        "items": fields.List(fields.Nested(
            ns.model(
                "items",
                {
                    "id": fields.String(required=True),
                    "quantity": fields.Integer(required=True),
                    "updatedAt": fields.Integer(required=True),
                }
            )
        ))
    }
)