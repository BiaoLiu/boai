# coding:utf-8
from django.contrib import auth
from django.contrib.auth.decorators import login_required
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
        user_id = kwargs.get('user_id')
        return render(request, self.template_name, {'user_id': user_id})

    def post(self, request, *args, **kwargs):
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
            # 登录 cookie默认保存两周
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


@login_required
def usertest(request):
    url = reverse('wechat:register', kwargs={'body': 'foo'})

    # return render(request, 'user/user_test.html')

    return redirect(to=url, *[1, 2, 3])


class UserInfoView(View):
    template_name = 'user/baseuserinfo.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass

    def login(self, request):
        pass


class OrderDetailView(View):
    template_name = 'user/order_detail.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass

    def login(self, request):
        pass


class BuJiaoView(View):
    template_name = 'user/bujiao.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass

    def login(self, request):
        pass
