# coding: utf-8

from functools import wraps
from .http import JSONResponse, JSONError


def request_validate(serializer_form):
    '''通用请求参数处理'''

    def decorator(func):
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            form = serializer_form(request.POST)
            if not form.is_valid():
                error_string = [value[0] for key, value in form.errors.items()][0]
                return JSONError(error_string)
            kwargs['form'] = form
            return func(self, request, *args, **kwargs)

        return wrapper

    return decorator
