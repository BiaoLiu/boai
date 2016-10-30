# coding:utf-8
from django.shortcuts import render
from django.views.generic import View
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import authentication

from boai.apps.boai_model.models import AppSocialPrice
from boai.apps.wechat.serializers.social import SocialSerializer
from boai.libs.common.http import JSONError, JSONResponse
from boai.libs.common.response import res_msg, res_code
from ..services.social import SocialService


class SocialView(View):
    template_name = 'user/wuxian1.html'

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


class SocialViewSet(viewsets.ModelViewSet):
    authentication_classes = (authentication.SessionAuthentication,)
    queryset = AppSocialPrice.objects.all()

    @list_route(url_path='getsocialprice')
    def get_social_price(self, request, *args, **kwargs):
        user_id = request.GET.get('user_id')
        social_type = request.GET.get('social_type')

        social_service = SocialService()
        result = social_service.get_social_price(social_type, '深圳')
        if len(result.ruleviolations) > 0:
            res_msg['recode'] = res_code['error']
            res_msg['msg'] = result.ruleviolations[0].error_message
            res_msg['data'] = ''
        else:
            res_msg['recode'] = res_code['success']
            res_msg['msg'] = ''
            res_msg['data'] = SocialSerializer(result.data).data

        return Response(res_msg)
