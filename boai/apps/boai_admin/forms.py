# coding: utf-8
from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from boai.apps.boai_model.models import AuthUser


class UserForm(forms.ModelForm):
    realname = forms.CharField(max_length=20, required=False)
    idcart = forms.CharField(max_length=20, required=False)

    # social_city = forms.CharField(max_length=20, blank=True, null=True)

    def __init__(self, *args, **kwargs):
        user = kwargs['instance']

        kwargs['initial'] = {
            'realname': user.profile.realname,
            'idcart': user.profile.idcart
        }

        super(UserForm, self).__init__(**kwargs)

    class Meta:
        model = AuthUser
        exclude = ('',)


class BoaiUserCreationForm(UserCreationForm):
    realname = forms.CharField(label='姓名', max_length=20, required=False)
    idcart = forms.CharField(label='身份证号码', max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        super(BoaiUserCreationForm, self).__init__(*args, **kwargs)
        # self.fields['email'].required = True  # 为了让此字段在admin中为必选项，自定义一个form


class BoaiUserChangeForm(UserChangeForm):
    realname = forms.CharField(label='姓名', max_length=20, required=False)
    idcart = forms.CharField(label='身份证号码', max_length=20, required=False)

    def __init__(self, *args, **kwargs):
        user = kwargs['instance']
        kwargs['initial'] = {
            'realname': user.profile.realname,
            'idcart': user.profile.idcart
        }
        super(BoaiUserChangeForm, self).__init__(*args, **kwargs)
        self.fields['email'].required = True
