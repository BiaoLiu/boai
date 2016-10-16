# coding: utf-8
from django.contrib.auth.backends import ModelBackend

from model.models import AuthUser


class WechatBackend(ModelBackend):
    def authenticate(self, username):
        try:
            user = AuthUser.objects.get(username=username)
        except AuthUser.DoesNotExist:
            return None

        return user
