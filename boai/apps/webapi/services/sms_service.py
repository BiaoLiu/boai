# coding: utf-8
import random

from boai.apps.boai_model.models import AppSendsms

from boai.libs.utility import sms_server

VERIFY_TEXT = '您的验证码是：{0}'


class SmsService:
    @staticmethod
    def send_code(mobile):
        '''
        发送手机验证码
        :param mobile:
        :return:
        '''
        verify_code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        content = VERIFY_TEXT.format(verify_code)
        is_success = sms_server.send_sms(mobile, content)
        if is_success:
            sms = AppSendsms(mobile=mobile, captcha=verify_code, content=content, is_success=True)
            sms.save()

        return is_success
