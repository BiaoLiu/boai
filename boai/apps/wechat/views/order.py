# coding: utf-8
from braces.views import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import View

from boai.apps.boai_model.models import AppSalesorders
from boai.libs.common.boai_enum import OrderStatus


class PayOrderView(LoginRequiredMixin, ListView):
    template_name = 'order/pay_order.html'
    context_object_name = 'order_list'

    queryset = AppSalesorders.objects.filter(orderstatus=OrderStatus.Paid.value)

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user_id=request.user.id)
        return super(PayOrderView, self).get(request, *args, **kwargs)


class PayOrderDetailView(DetailView):
    template_name = 'order/pay_order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    queryset = AppSalesorders.objects.filter(orderstatus=OrderStatus.Paid.value)

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user_id=request.user.id)
        return super(PayOrderDetailView, self).get(request, *args, **kwargs)


class UnPayOrderView(LoginRequiredMixin, ListView):
    template_name = 'order/unpay_order.html'
    context_object_name = 'order_list'

    queryset = AppSalesorders.objects.filter(orderstatus=OrderStatus.UnPaid.value)

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user_id=request.user.id)
        return super(UnPayOrderView, self).get(request, *args, **kwargs)


class UnPayOrderDetailView(DetailView):
    template_name = 'order/unpay_order_detail.html'
    context_object_name = 'order'
    pk_url_kwarg = 'order_id'

    queryset = AppSalesorders.objects.filter(orderstatus=OrderStatus.UnPaid.value)

    def get(self, request, *args, **kwargs):
        self.queryset = self.queryset.filter(user_id=request.user.id)
        return super(UnPayOrderDetailView, self).get(request, *args, **kwargs)
