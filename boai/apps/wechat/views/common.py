# coding: utf-8
from datetime import datetime

from django.http import HttpResponse
from django.views.decorators.http import require_GET
from django.core.cache import cache
from boai.apps.webapi.services.sms_service import SmsService
from boai.apps.wechat.forms import VerifycodeForm
from boai.libs.common.response import APIResponse
from boai.libs.utility.redis_con import redis


@require_GET
def get_verifycode(request):
    '''
    获取手机验证码'
    '''
    resp = APIResponse()

    form = VerifycodeForm(request.GET)
    if not form.is_valid():
        resp.set_status(False, '手机号码有误')
        return HttpResponse(resp.to_json())

    # test = cache.keys('*')
    mobile = form.cleaned_data.get('mobile')

    flag = redis.get('s:code:' + mobile)
    if flag:
        resp.set_status(False, '获取验证码过于频繁，请稍后再试')
    else:
        is_success = SmsService.send_code(mobile)
        if is_success:
            redis.set('s:code:' + mobile, datetime.now(), 30)
        resp.set_status(is_success, '获取验证码出错，请稍后再试' if not is_success else '')

    return HttpResponse(resp.to_json())
