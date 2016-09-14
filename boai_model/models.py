from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from boai import settings


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
    nickname = models.CharField('昵称', max_length=40, blank=True, null=True)
    mobile = models.CharField('手机', max_length=20, null=True)
    avatar = models.CharField('头像', max_length=200, default='')

    objects = AuthUserManager()

    class Meta:
        db_table = 'auth_user'


class AppUserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
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


class AppPlatformUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    nickname = models.CharField(max_length=40, blank=True, null=True)
    avatar = models.CharField(max_length=200, blank=True, null=True)
    platform = models.CharField(max_length=20, blank=True, null=True)
    openid = models.CharField(max_length=40, blank=True, null=True)
    unionid = models.CharField(max_length=40, blank=True, null=True)
    access_token = models.CharField(max_length=40, blank=True, null=True)
    refresh_token = models.CharField(max_length=40, blank=True, null=True)
    expirationtime = models.DateTimeField(blank=True, null=True)
    profileurl = models.CharField(max_length=200, blank=True, null=True)
    ts = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'app_platform_user'
