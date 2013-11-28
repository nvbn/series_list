from copy import copy
from requests import Timeout
from decorator import decorator


def return_if_timeout(return_value_or_method, is_method=False):
    """Return value if timeout"""
    @decorator
    def return_if_timeout_decorator(fnc, *args, **kwargs):
        try:
            return fnc(*args, **kwargs)
        except Timeout:
            if is_method:
                return getattr(args[0], return_value_or_method)()
            else:
                return copy(return_value_or_method)
    return return_if_timeout_decorator
