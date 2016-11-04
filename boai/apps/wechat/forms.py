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
        self.user = None
        super(RegisterForm, self).__init__(*args, **kwargs)

    def clean_user_id(self):
        user_id = self.cleaned_data.get('user_id')
        try:
            self.user = AuthUser.objects.get(id=user_id)
        except AuthUser.DoesNotExist:
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
    idcart = forms.IntegerField()
    email = forms.EmailField()
    social_city = forms.CharField()
    household_type = forms.CharField()
    cpf_count = forms.IntegerField(required=False)


SOCIAL_TYPE = (
    ('shenhu_first', '深户第一档'),
    ('feishenhu_first', '非深户第一档'),
    ('feishenhu_second', '非深户第二档'),
    ('feishenhu_third', '非深户第三档')
)


class SocialOrderForm(forms.Form):
    # user_id = forms.IntegerField()
    social_type = forms.ChoiceField(choices=SOCIAL_TYPE)
    is_social = forms.BooleanField()
    is_fund = forms.BooleanField()
    social_base = forms.DecimalField(required=False, min_value=2030, max_value=20259, max_digits=18, decimal_places=2)
    fund_base = forms.DecimalField(required=False, min_value=2030, max_value=33765, max_digits=18, decimal_places=2)
    startmonth = forms.DateTimeField()
    endmonth = forms.DateTimeField()

    def clean(self):
        is_social = self.cleaned_data.get('is_social')
        is_fund = self.cleaned_data.get('is_fund')

        if not is_social and not is_fund:
            raise forms.ValidationError('请选择缴纳社保或公积金')
