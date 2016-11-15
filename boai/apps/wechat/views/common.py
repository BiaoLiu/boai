# coding: utf-8
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.core.cache import cache
from boai.apps.webapi.services.sms_service import SmsService
from boai.libs.common.response import APIResponse
from boai.libs.utility.redis_con import redis


@require_GET
def get_verifycode(request):
    '''
    获取手机验证码'
    '''

    resp = APIResponse()

    # test = cache.keys('*')

    mobile = request.GET.get('mobile')

    is_success = redis.get('s:code:' + mobile)
    if is_success:
        resp.set_status(False, '获取验证码过于频繁，请稍后再试')
    else:
        if mobile:
            is_success = SmsService.send_code(mobile)

        resp.set_status(is_success, '获取验证码出错，请稍后再试' if not is_success else '')

    return HttpResponse(resp.to_json(), content_type='application/json')
