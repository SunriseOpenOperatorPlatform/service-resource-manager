from typing import List

import time
import base64
import connexion
from jose import JWTError, jwt
from werkzeug.exceptions import Unauthorized

JWT_ISSUER = "com.icom-telecom.connexion"
JWT_SECRET = "pi-edge-platform"
JWT_LIFETIME_SECONDS = 7200 #expires in 2 hours
JWT_ALGORITHM = "HS256"

"""
controller generated to handled auth operation described at:
https://connexion.readthedocs.io/en/latest/security.html

https://connexion.readthedocs.io/en/latest/request.html

"""
def check_api_key(api_key, required_scopes):
    return {'test_key': 'test_value'}

def check_registry_auth(token):
    return {'scopes': ['read:pets', 'write:pets'], 'uid': 'test_value'}

def validate_scope_registry_auth(required_scopes, token_scopes):
    return set(required_scopes).issubset(set(token_scopes))



def generate_token(user_id):
    timestamp = _current_timestamp()
    payload = {
        "iss": JWT_ISSUER,
        "iat": int(timestamp),
        "exp": int(timestamp + JWT_LIFETIME_SECONDS),
        "sub": str(user_id),
    }

    # x=base64.b64encode("nikos".encode("utf - 8"))
    # print(x)
    # y=base64.b64decode(x).decode("utf - 8")
    # print(y)

    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token):
    try:
        return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except JWTError as e:
        raise Unauthorized from e


def get_secret(user, token_info) -> str:
    return """
    You are user_id {user} and the secret is 'wbevuec'.
    Decoded token claims: {token_info}.
    """.format(
        user=user, token_info=token_info
    )


def _current_timestamp() -> int:
    return int(time.time())
