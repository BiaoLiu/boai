from django.conf.urls import url
from django.views.generic import TemplateView
from .views import views, user

from boai_wechat.views import views as boai_wechat_views

urlpatterns = [
    # url(r'^$', boai_wechat_views.index),
    url(r'^set_menu$', boai_wechat_views.create_menu),

    url(r'', views.main,name='main'),

    url(r'^login/$', user.LoginView.as_view(), name='login'),

]
