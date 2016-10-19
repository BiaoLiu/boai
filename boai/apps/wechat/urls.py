from django.conf.urls import url

from .views import wechat as boai_wechat_views
from .views import wechat, user

urlpatterns = [
    # url(r'^$', boai_wechat_views.index),
    url(r'^set_menu$', boai_wechat_views.create_menu),

    url(r'^jsapi_code/$', wechat.jsapi_code),

    url(r'^$', wechat.main, name='main'),
    url(r'^main/$', wechat.main),

    url(r'^register/$', user.Register.as_view(), name='register'),

    url(r'^login/$', user.LoginView.as_view(), name='login'),

    url(r'^userinfo/$', user.UserInfoView.as_view(), name='userinfo'),

    url(r'^orderdetail/$', user.OrderDetailView.as_view(), name='orderdetail'),

    url(r'^bujiao/$', user.BuJiaoView.as_view(), name='bujiao'),

    url(r'^usertest/$', user.usertest)

]
