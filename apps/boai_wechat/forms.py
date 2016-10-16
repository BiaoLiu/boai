# coding:utf-8
from django import forms
from django.contrib import auth


class LoginForm(forms.Form):
    username = forms.CharField(max_length=20)
    verifycode = forms.IntegerField()

    error_messages = {'invalid_login': '用户名错误',
                      'inactive': '用户未激活'}

    def __init__(self, *args, **kwargs):
        self.user_cache = None
        super(LoginForm, self).__init__(*args, **kwargs)

    # def clean_username(self):
    #     pass

    def clean(self):
        username = self.cleaned_data.get('username')
        verifycode = self.cleaned_data.get('verifycode')

        self.user_cache = auth.authenticate(username=username)
        if not self.user_cache:
            raise forms.ValidationError(self.error_messages['invalid_login'])

        if not self.user_cache.is_active:
            raise forms.ValidationError(self.error_messages['inactive'])

    def get_user(self):
        return self.user_cache
