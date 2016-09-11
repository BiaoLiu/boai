# coding: utf-8

from rest_framework import viewsets
from rest_framework.decorators import list_route
from rest_framework.response import Response
from rest_framework import permissions
# from boai_model.models import AppStock
from boai_model.models import AppStock


class MainViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = AppStock.objects.all()

    @list_route(url_path='getstocklist')
    def get_stocklist(self, request, *args, **kwargs):
        return Response({'data': 'ok'})

