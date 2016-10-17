# coding:utf-8
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views.generic import View, ListView
from ..forms import LoginForm, RegisterForm
from boai.libs.common.http import JSONResponse, JSONError


class Register(View):
    template_name = 'user/register.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            # 登录 cookie默认保存15天
            auth.login(request, form.get_user())
            return JSONResponse()

        error_string = [value[0] for key, value in form.errors.items()][0]
        return JSONError(error_string)


class LoginView(View):
    template_name = 'user/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            # 登录 cookie默认保存15天
            auth.login(request, form.get_user())
            return JSONResponse()

        # ErrorDict、ErrorList
        # for k, v in form.errors.items():
        #     t = v[0]

        error_string = [value[0] for key, value in form.errors.items()][0]
        return JSONError(error_string)


class UserView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def login(self, request):
        pass


def usertest(request):
    return render(request, 'user/user_test.html')


class UserInfoView(View):
    template_name = 'user/baseuserinfo.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass

    def login(self, request):
        pass
