"""JSON helper functions"""
from boai.libs.common.response import res_code, res_msg

try:
    import simplejson as json
except ImportError:
    import json

from django.http import HttpResponse


def JsonResponse(data=None, dump=True, success=True, msg='', status=200):
    # try:
    #     data['errors']
    # except KeyError:
    #     data['success'] = True
    # except TypeError:
    #     pass
    if success:
        res_msg['recode'] = res_code['success']
        res_msg['msg'] = '操作成功'
        res_msg['data'] = data if data else ''
        return Response(res_msg, dump, status)
    else:
        return JsonError(msg, status=status)


def JsonError(error_string, status=200):
    res_msg['recode'] = res_code['error']
    res_msg['msg'] = error_string if error_string else '请求出错,请稍后再试！'
    res_msg['data'] = ''

    return Response(res_msg, status=status)


def Response(data, dump=True, status=200):
    return HttpResponse(
        json.dumps(data, ensure_ascii=False) if dump else data,
        content_type='application/json',
        status=status,
    )


def JsonResponseBadRequest(error_string):
    return JsonError(error_string, status=400)


def JsonResponseUnauthorized(error_string):
    return JsonError(error_string, status=401)


def JsonResponseForbidden(error_string):
    return JsonError(error_string, status=403)


def JsonResponseNotFound(error_string):
    return JsonError(error_string, status=404)


def JsonResponseNotAllowed(error_string):
    return JsonError(error_string, status=405)


def JsonResponseNotAcceptable(error_string):
    return JsonError(error_string, status=406)


# For backwards compatability purposes
JSONResponse = JsonResponse
JSONError = JsonError
