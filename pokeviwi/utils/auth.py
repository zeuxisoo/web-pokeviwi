import functools
from flask import session, jsonify

def require_login(method):
    @functools.wraps(method)
    def wrapper(*args, **kwargs):
        print(session)
        if 'username' not in session:
            return jsonify(
                ok      = False,
                message = "Please sign in first"
            ), 401
        else:
            return method(*args, **kwargs)
    return wrapper
