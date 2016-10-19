# coding:utf-8
from django import forms
from django.contrib import auth

from boai.apps.boai_model.models import AuthUser, AppUserProfile


class RegisterForm(forms.Form):
    user_id = forms.IntegerField()
    mobile = forms.IntegerField()
    verifycode = forms.IntegerField()
    password = forms.CharField(min_length=6)
    password2 = forms.CharField(min_length=6)

    error_messages = {'id_notexists': 'id不存在',
                      'mobile_exists': '手机号码已注册',
                      'password_notconsistent': '密码不一致',
                      'verficode_error': '验证码错误'}

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        self.user_cache = AuthUser.objects.filter(id=user_id)
        if not self.user_cache:
            raise forms.ValidationError(self.error_messages['id_notexists'])


def clean_password2(self):
    password = self.cleaned_data.get('password')
    password2 = self.cleaned_data.get('password2')

    if password != password2:
        raise forms.ValidationError(self.error_messages['password_notconsistent'])


def clean(self):
    mobile = self.cleaned_data.get('mobile')
    password = self.cleaned_data.get('password')
    verifycode = self.cleaned_data.get('verifycode')

    if not mobile or not password or not verifycode or not self.user:
        return

    user = AuthUser.objects.filter(mobile=mobile)
    if user:
        raise forms.ValidationError(self.error_messages['mobile_exists'])

    # todo 验证码校验

    self.user.mobile = mobile
    self.user.username = mobile
    self.user.set_password(password)
    self.user.save()

    self.user = auth.authenticate(username=mobile)


def get_user(self):
    return self.user


class LoginForm(forms.Form):
    username = forms.CharField()
    verifycode = forms.IntegerField()

    error_messages = {'invalid_login': '用户名错误',
                      'inactive': '用户未激活'}

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        username = self.cleaned_data.get('username')
        verifycode = self.cleaned_data.get('verifycode')

        if not username or not verifycode:
            return

        self.user_cache = auth.authenticate(username=username)
        if not self.user_cache:
            raise forms.ValidationError(self.error_messages['invalid_login'])

        if not self.user_cache.is_active:
            raise forms.ValidationError(self.error_messages['inactive'])

    def get_user(self):
        return self.user_cache
