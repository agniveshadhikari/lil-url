from functools import wraps
from flask import (
    request,
    g as request_context,
    abort)


def check_access(access_level):

    def decorator(func):

        @wraps(func)
        def wrapped(*args, **kwargs):
            user = request_context.user
            if user.access_level != access_level:
                print(f"User {user.username} unauthorized for request to {request.path}. Required access_level={access_level}, actual access_level={user.access_level}")
                return abort(403)

            return func(*args, **kwargs)

        return wrapped

    return decorator
