# coding:utf-8
from datetime import datetime

from django import forms
from django.contrib import auth

from boai.apps.boai_model.models import AuthUser, AppUserProfile


class RegisterForm(forms.Form):
    user_id = forms.IntegerField()
    mobile = forms.IntegerField()
    verifycode = forms.IntegerField()
    password = forms.CharField(min_length=8)
    password2 = forms.CharField(min_length=8)

    error_messages = {'id_notexists': 'id不存在',
                      'mobile_exists': '手机号码已注册',
                      'password_notconsistent': '密码不一致',
                      'verficode_error': '验证码错误'}

    def __init__(self, *args, **kwargs):
        self.user = None
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        try:
            self.user = AuthUser.objects.get(id=user_id)
        except AuthUser.DoesNotExist:
            raise forms.ValidationError(self.error_messages['id_notexists'])
        return user_id

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

    def get_user(self):
        return self.user


class LoginForm(forms.Form):
    mobile = forms.IntegerField()
    verifycode = forms.IntegerField()

    error_messages = {'invalid_login': '用户不存在',
                      'inactive': '用户未激活'}

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    def clean(self):
        mobile = self.cleaned_data.get('mobile')
        verifycode = self.cleaned_data.get('verifycode')

        if not mobile or not verifycode:
            return

        self.user_cache = auth.authenticate(username=mobile)
        if not self.user_cache:
            raise forms.ValidationError(self.error_messages['invalid_login'])

        if not self.user_cache.is_active:
            raise forms.ValidationError(self.error_messages['inactive'])

    def get_user(self):
        return self.user_cache


class UserInfoForm(forms.Form):
    user_id = forms.IntegerField()
    realname = forms.CharField()
    idcart = forms.CharField()
    email = forms.EmailField()
    social_city = forms.CharField()
    household_type = forms.CharField()
    # cpf_count = forms.IntegerField(required=False)


SOCIAL_TYPE = (
    ('shenhu_first', '深户第一档'),
    ('feishenhu_first', '非深户第一档'),
    ('feishenhu_second', '非深户第二档'),
    ('feishenhu_third', '非深户第三档')
)


class SocialOrderForm(forms.Form):
    # user_id = forms.IntegerField()
    social_type = forms.ChoiceField(choices=SOCIAL_TYPE)
    is_social = forms.IntegerField()
    is_fund = forms.IntegerField()
    social_base = forms.DecimalField(required=False, min_value=2030, max_value=20259, max_digits=18, decimal_places=2)
    fund_base = forms.DecimalField(required=False, min_value=2030, max_value=33765, max_digits=18, decimal_places=2)
    startmonth = forms.DateTimeField()
    endmonth = forms.DateTimeField()

    error_message = {
        'invalid_date': '缴纳月份有误'
    }

    def clean(self):
        is_social = self.cleaned_data.get('is_social')
        is_fund = self.cleaned_data.get('is_fund')

        if not is_social and not is_fund:
            raise forms.ValidationError('请选择缴纳社保或公积金')

    def clean_startmonth(self):
        startmonth = self.cleaned_data.get('startmonth')
        now = datetime.now()

        if (startmonth.year < now.year):
            raise forms.ValidationError(self.error_message['invalid_date'])

        if startmonth.year == now.year:
            if startmonth.month < now.month:
                raise forms.ValidationError(self.error_message['invalid_date'])
            elif startmonth.month == now.month and now.day >= 20:
                raise forms.ValidationError('当前月已超过缴纳时间')

        return startmonth

    def clean_endmonth(self):
        startmonth = self.cleaned_data.get('startmonth')
        endmonth = self.cleaned_data.get('endmonth')

        if endmonth < startmonth:
            raise forms.ValidationError(self.error_message['invalid_date'])

        return endmonth
