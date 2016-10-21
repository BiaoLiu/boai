# coding:utf-8
from .http import JSONResponse, JSONError


def request_validate(serializer_form):
    '''
    :param 需要校验的form类
    '''
    def decorator(func):
        def in_decorator(self, request, *args, **kwargs):
            form = serializer_form(request.POST)
            if not form.is_valid():
                error_string = [value[0] for key, value in form.errors.items()][0]
                return JSONError(error_string)
            kwargs['form'] = form
            return func(self, request, *args, **kwargs)

        return in_decorator

    return decorator
