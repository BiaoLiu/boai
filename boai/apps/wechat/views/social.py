#coding:utf-8
from django.shortcuts import render
from django.views.generic import View


class SocialView(View):
    template_name = 'user/social.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass
