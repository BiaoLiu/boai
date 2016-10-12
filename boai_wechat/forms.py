#coding:utf-8
from django import forms

class LoginForm(forms.Form):
    username=forms.CharField(max_length=20)
    password=forms.CharField()

    error_messages={'invalid_login':'用户名或密码错误',
                    'inactive':'用户未激活'}

    # def clean_username(self):
    #     pass

    def clean(self):
        username=self.cleaned_data.get('username')
        password=self.cleaned_data.get('password')

        if(username!='lbi'):
            raise forms.ValidationError(self.error_messages['invalid_login'])

