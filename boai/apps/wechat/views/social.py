#coding:utf-8
from django.shortcuts import render
from django.views.generic import View


class SocialView(View):
    template_name = 'user/social.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass


class BuJiaoView(View):
    template_name = 'user/bujiao.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass


def get_socialprice(request):
    city= request.GET.get('city')
    type=request.GET.get('type')