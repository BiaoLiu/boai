# coding:utf-8
from django.conf.urls import url

from boai_webapi.views.views import ApiEndpoint

urlpatterns = [
    url('^hello$', ApiEndpoint.as_view())
]
