# coding: utf-8
from django.shortcuts import render
from django.views.generic import View


class OrderDetailView(View):
    template_name = 'user/order_detail.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass