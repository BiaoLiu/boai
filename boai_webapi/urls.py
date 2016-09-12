# coding:utf-8
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from boai_webapi.views.main import MainViewSet
from boai_webapi.views.views import ApiEndpoint, test

router = DefaultRouter()
router.register('main', MainViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^hello$', ApiEndpoint.as_view()),
    url(r'^test', test),
]
