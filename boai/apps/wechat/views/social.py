# coding:utf-8
from django.shortcuts import render
from django.views.generic import View
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import authentication

from boai.apps.boai_model.models import AppSocials
from boai.apps.wechat.serializers.social import SocialSerializer
from boai.libs.common.http import JSONError, JSONResponse
from boai.libs.common.response import res_msg, res_code
from boai.libs.common.request_validate import request_validate
from ..services.social import SocialService
from ..services.order import OrderService
from ..forms import SocialOrderForm
from ..compat import LoginRequiredMixin


class SocialView(LoginRequiredMixin, View):
    template_name = 'social/wuxian.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    @request_validate(SocialOrderForm)
    def post(self, request, *args, **kwargs):
        form = kwargs['form'].cleaned_data
        order_service = OrderService()
        result = order_service.create_social_order(request.user.id, **form)

        if not result.error_is_empty:
            return JSONError(result.ruleviolations[0].error_message)
        return JSONResponse(result.data)


class BuJiaoView(View):
    template_name = 'social/bujiao.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        pass


class SocialViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.SessionAuthentication,)
    queryset = AppSocials.objects.all()

    @list_route(url_path='getsocialprice')
    def get_social_price(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        social_type = request.GET.get('social_type')

        social_service = SocialService()
        result = social_service.get_social_price(social_type, '深圳')
        if not result.error_is_empty:
            res_msg['recode'] = res_code['error']
            res_msg['msg'] = result.ruleviolations[0].error_message
            res_msg['data'] = ''
        else:
            res_msg['recode'] = res_code['success']
            res_msg['msg'] = ''
            res_msg['data'] = SocialSerializer(result.data).data

        return Response(res_msg)
