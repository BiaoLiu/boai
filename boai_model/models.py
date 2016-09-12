#coding:utf-8
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from boai import settings

# 管理类
class AuthUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        '''创建user'''
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=AuthUserManager.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)

        # 添加用户详细信息
        user_profile = AppUserProfile(user_id=user.id)
        user_profile.save()

        return user

    def create_superuser(self, email, username, password):
        '''创建超级管理员'''
        user = self.create_user(email,
                                username=username,
                                password=password,
                                )

        user.is_staff = True
        user.is_active = True
        user.is_admin = True
        user.save(using=self._db)

        return user

class AuthUser(AbstractUser):
    mobile = models.CharField('手机', max_length=20, null=True)
    avatar = models.CharField('头像', max_length=200, default='')

    objects = AuthUserManager()

    class Meta:
        db_table = 'auth_user'


class AppUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True)
    realname = models.CharField(max_length=20, blank=True, null=True)
    idcart = models.CharField(max_length=20, blank=True, null=True)
    social_province = models.CharField(max_length=20, blank=True, null=True)
    social_city = models.CharField(max_length=20, blank=True, null=True)
    idcart_front = models.CharField(max_length=200, blank=True, null=True)
    idcart_back = models.CharField(max_length=200, blank=True, null=True)
    household_type = models.CharField(max_length=20, blank=True, null=True)
    cpf_account = models.CharField(max_length=20, blank=True, null=True)
    bank_account = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'app_user_profile'



