from django.conf.urls import url
from django.views.generic import TemplateView

from .views import wechat as boai_wechat_views
from .views import wechat, user

urlpatterns = [
    # url(r'^$', boai_wechat_views.index),
    url(r'^set_menu$', boai_wechat_views.create_menu),



    url(r'^jsapi/$', wechat.jsapi),
    url(r'^get_jsapi_authorize/$', wechat.get_jsapi_authorize, name='jsapi_authorize'),

    url(r'^$', wechat.main, name='main'),
    url(r'^main/$', wechat.main),

    url(r'^register/(?P<user_id>\d+)$', user.Register.as_view(), name='register', kwargs={'test': ''}),

    url(r'^login/$', user.LoginView.as_view(), name='login'),

    url(r'^userinfo/$', user.UserInfoView.as_view(), name='userinfo'),

    url(r'^orderdetail/$', user.OrderDetailView.as_view(), name='orderdetail'),

    url(r'^bujiao/$', user.BuJiaoView.as_view(), name='bujiao'),

    url(r'^usertest/$', user.usertest)

]
