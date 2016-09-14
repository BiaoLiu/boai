# coding: utf-8
import random

from boai_utility import sms

VERIFY_TEXT = '您的验证码是：{0}'


class SmsService:
    def send_code(self, mobile):
        verify_code = [random.randint(0, 9) for _ in range(6)]
        sms.send_sms(VERIFY_TEXT.format(verify_code),mobile)

