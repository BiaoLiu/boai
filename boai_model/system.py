# coding:utf-8
from django.db import models

class AppSendsms(models.Model):
    sms_id = models.CharField(primary_key=True, max_length=40)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    captcha = models.CharField(max_length=20, blank=True, null=True)
    device_id = models.CharField(max_length=20, blank=True, null=True)
    is_success = models.CharField(max_length=40, blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'app_sendsms'