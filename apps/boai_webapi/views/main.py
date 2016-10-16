# coding: utf-8
from rest_framework import viewsets
from rest_framework.response import Response

from boai_model.models import AuthUser


class MainViewSet(viewsets.ModelViewSet):
    # permission_classes = [permissions.IsAuthenticated]
    queryset = AuthUser.objects.all()

    def get_stocklist(self, request, *args, **kwargs):
        return Response({'data': 'ok'})

