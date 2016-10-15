# coding:utf-8
from django.contrib import auth
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.response import TemplateResponse
from django.views.generic import View, ListView
from ..forms import LoginForm


class LoginView(View):
    template_name = 'user/login.html'

    def get(self, request, *args, **kwargs):
        # return HttpResponse()
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            # 登录 cookie默认保存15天
            auth.login(request, form.get_user())
            return redirect(reverse('wechat:main'))

        data = form.errors
        # data2=data['username']

        context = {'form': form}

        return render(request, self.template_name, context)


class UserView(View):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def login(self, request):
        pass


def usertest(request):
    return render(request,'user/user_test.html')

class UserInfoView(View):
    template_name = 'user/userinfo.html'
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass

    def login(self, request):
        pass