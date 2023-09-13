"""authentication"""
import json
import os
from functools import wraps

from flask import request
from jose import jwt
from six.moves.urllib.request import urlopen

from api.errors import Error


def get_token_auth_header() -> str:
    """Obtains the access token from the Authorization Header"""
    auth = request.headers.get("Authorization", None)
    if not auth:
        raise Error(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected",
            },
            401,
        )

    parts = auth.split()

    if parts[0].lower() != "bearer":
        raise Error(
            {
                "code": "invalid_header",
                "description": "Authorization header must start with" " Bearer",
            },
            401,
        )
    if len(parts) == 1:
        raise Error({"code": "invalid_header", "description": "Token not found"}, 401)
    if len(parts) > 2:
        raise Error(
            {
                "code": "invalid_header",
                "description": "Authorization header must be" " Bearer token",
            },
            401,
        )

    token = parts[1]
    return token


def requires_token(func):
    """Determines if the access token is valid"""

    @wraps(func)
    def decorated(*args, **kwargs):
        token = get_token_auth_header()
        jsonurl = urlopen(
            "https://" + os.getenv("AUTH0_DOMAIN") + "/.well-known/jwks.json"
        )
        jwks = json.loads(jsonurl.read())
        try:
            unverified_header = jwt.get_unverified_header(token)
        except jwt.JWTError as jwt_error:
            raise Error(
                {
                    "code": "invalid_header",
                    "description": "Invalid header. "
                    "Use an RS256 signed JWT Access Token",
                },
                401,
            ) from jwt_error
        if unverified_header["alg"] == "HS256":
            raise Error(
                {
                    "code": "invalid_header",
                    "description": "Invalid header. "
                    "Use an RS256 signed JWT Access Token",
                },
                401,
            )
        rsa_key = {}
        for key in jwks["keys"]:
            if key["kid"] == unverified_header["kid"]:
                rsa_key = {
                    "kty": key["kty"],
                    "kid": key["kid"],
                    "use": key["use"],
                    "n": key["n"],
                    "e": key["e"],
                }
        if rsa_key:
            try:
                payload = jwt.decode(
                    token,
                    rsa_key,
                    algorithms=os.getenv("ALGORITHMS"),
                    audience=os.getenv("API_IDENTIFIER"),
                    issuer="https://" + os.getenv("AUTH0_DOMAIN") + "/",
                )
            except jwt.ExpiredSignatureError as expired_sign_error:
                raise Error(
                    {"code": "token_expired", "description": "token is expired"}, 401
                ) from expired_sign_error
            except jwt.JWTClaimsError as jwt_claims_error:
                raise Error(
                    {
                        "code": "invalid_claims",
                        "description": "incorrect claims,"
                        " please check the audience and issuer",
                    },
                    401,
                ) from jwt_claims_error
            except Exception as exc:
                raise Error(
                    {
                        "code": "invalid_header",
                        "description": "Unable to parse authentication" " token.",
                    },
                    401,
                ) from exc
            print(payload)
            user_sub = payload.get("sub")
            return func(user_sub=user_sub, *args, **kwargs)
        raise Error(
            {"code": "invalid_header", "description": "Unable to find appropriate key"},
            401,
        )

    return decorated


def get_apikey_auth_header() -> str:
    """Obtains the apiKey from Header"""
    api_key = request.headers.get("apiKey", None)
    if not api_key:
        raise Error(
            {
                "code": "invalid_header",
                "description": "apiKey not found.",
            },
            401,
        )
    return api_key


def requires_api_key(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        api_key = get_apikey_auth_header()
        if api_key != os.getenv("API_KEY"):
            raise Error(
                {
                    "code": "invalid_header",
                    "description": "apiKey mismatch.",
                },
                401,
            )
        return func(*args, **kwargs)

    return decorated
