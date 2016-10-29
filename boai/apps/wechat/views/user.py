# coding:utf-8
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views.generic import View, ListView

from boai.apps.boai_model.models import AuthUser
from boai.libs.common.request_validate import request_validate
from boai.libs.common.http import JSONResponse
from ..compat import LoginRequiredMixin
from ..forms import LoginForm, RegisterForm, UserInfoForm
from ..services.user import UserService


class Register(LoginRequiredMixin, View):
    template_name = 'user/register.html'

    def get(self, request, *args, **kwargs):
        user_id = kwargs.get('user_id')
        return render(request, self.template_name, {'user_id': user_id})

    @request_validate(RegisterForm)
    def post(self, request, *args, **kwargs):
        form = kwargs.get('form')
        cleaned_data = form.cleaned_data
        # 保存注册信息
        user = form.get_user()
        user.username = user.mobile = cleaned_data.get('mobile')
        user.set_password(cleaned_data.get('password'))
        user.save()

        return JSONResponse()


class LoginView(View):
    template_name = 'user/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    @request_validate(LoginForm)
    def post(self, request, *args, **kwargs):
        form = kwargs.get('form')
        # 登录 cookie默认保存两周
        auth.login(request, form.get_user())

        # ErrorDict、ErrorList
        # for k, v in form.errors.items():
        #     t = v[0]
        return JSONResponse()


@login_required
def usertest(request):
    url = reverse('wechat:register', kwargs={'body': 'foo'})

    # return render(request, 'user/user_test.html')
    return redirect(to=url, *[1, 2, 3])


class UserInfoView(LoginRequiredMixin, View):
    template_name = 'user/userinfo.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    @request_validate(UserInfoForm)
    def post(self, request, *args, **kwargs):
        form = kwargs.get('form').cleaned_data
        user_service = UserService()
        is_success = user_service.update_userinfo(**form)
        return JSONResponse(success=is_success)






