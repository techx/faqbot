from faqbot.config import SECRET
from functools import wraps

import datetime
import uuid
import jwt
import os

from flask import (
    redirect,
    request
)

DATE_FMT = "%Y-%m-%d %H:%M:%S"

def gen_uuid():
    """Generates a random UUID."""

    return str(uuid.uuid4()).replace('-', '')

def encode_token():
    """Encodes a JWT token with the current timestamp."""

    return jwt.encode({'timestamp': datetime.datetime.now().strftime(DATE_FMT),
                       'roll': gen_uuid()},
                       SECRET, algorithm='HS256')

def auth_request(request):
    """Main authentication routine, checks if auth token is valid."""
    if 'jwt' not in request.cookies:
        return False

    try:
        _ = datetime.datetime.strptime(
            jwt.decode(request.cookies['jwt'], SECRET, algorithms=['HS256'])['timestamp'], DATE_FMT)

        # TODO(revalo): Maybe don't issue infinite tokens?
        return True
    except Exception as _:
        return False
    
def requires_auth():
    """Decorator for Flask routes to check auth.
    """

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not auth_request(request):
                return redirect('/login')
            
            return f(*args, **kwargs)

        return decorated
    return decorator