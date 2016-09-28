# coding: utf-8
import random
import threading

from boai_model.models import AppSendsms
from src.boai_utility import sms_server

VERIFY_TEXT = '您的验证码是{0}'


class SmsService:
    @staticmethod
    def send_code(mobile):
        '''发送手机验证码'''
        verify_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        content = VERIFY_TEXT.format(verify_code)
        is_success = sms_server.send_sms(content, mobile)
        if is_success:
            sms = AppSendsms(mobile=mobile, captcha=verify_code, content=content, is_success=True)
            sms.save()
        return is_success
