# coding: utf-8
from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response

from boai_model.models import AuthUser
from boai_webapi.services.sms_service import SmsService


class MainViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = AuthUser.objects.all()

    def get_stocklist(self, request, *args, **kwargs):
        return Response({'data': 'ok'})

