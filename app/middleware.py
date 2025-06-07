from functools import wraps
from base64 import b64decode
from flask import request
from app.utils import authenticate, check_auth


def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get("Authorization")
        if not auth or not auth.lower().startswith("basic "):
            return authenticate()

        try:
            # Decode base64 string
            auth_decoded = b64decode(auth.split(" ")[1]).decode("utf-8")
            username, password = auth_decoded.split(":", 1)
        except Exception:
            return authenticate()

        if not check_auth(username, password):
            return authenticate()

        return f(*args, **kwargs)
    return decorated