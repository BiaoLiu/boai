# coding:utf-8
from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter

from .views import main,views

router = DefaultRouter()
router.register('main', main.MainViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^hello$', views.ApiEndpoint.as_view()),
    url(r'^test', views.test),
]
