from functools import wraps
from flask import session as login_session
from flask import redirect, url_for, request, Response, make_response
from app import SessionFields
import json
from types import FunctionType
from typing import Union, Any


def safe_get(dct: dict, *keys) -> Union[Any, None]:
    """
    A utility function to traverse dictionaries (JSON).

    Function based on discussion:

    http://stackoverflow.com/questions/25833613/python-safe-method-to-get-value-of-nested-dictionary

    :param dct:
    :param keys:
    :return Union[Any, None]: return either the target of the key path or None.
    """
    for key in keys:
        try:
            dct = dct[key]
        except (KeyError, TypeError):
            return None
    return dct


def check_login(f: FunctionType):
    """
    A decorator to test that a user has logged into the application.
    Args:
        f (FunctionType):

    Returns Union[FunctionType, Response]: Returns either the function to which
    the decorator has been applied or a Response indicating failure.

    """
    @wraps(f)
    def decorated_function(*args, **kwargs) -> Union[FunctionType, Response]:
        if not login_session[SessionFields.is_logged_in]:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function


def check_state(f: FunctionType) -> Union[FunctionType, Response]:
    """
    Create a decorator to test state.

    May only be used within a request context.

    :param f:
    :return Union[FunctionType, Response]: Returns either the function to which
    the decorator has been applied or a Response indicating failure.
    """

    @wraps(f)
    def decorated_function(*args, **kwargs) -> Union[FunctionType, Response]:
        if request.args.get('state') != login_session['state']:
            response = make_response(json.dumps('Invalid state'), 401)
            response.headers['Content-Type'] = 'application/json'
            return response
        return f(*args, **kwargs)
    return decorated_function

