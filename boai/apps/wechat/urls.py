from django.conf.urls import url
from django.views.generic import TemplateView

from .views import wechat, user, social

urlpatterns = [
    # url(r'^$', boai_wechat_views.index),
    url(r'^set_menu$', wechat.create_menu),

    url(r'^jsapi/$', wechat.jsapi),
    url(r'^get_jsapi_auth/$', wechat.get_jsapi_auth, name='jsapi_auth'),

    url(r'^$', wechat.main, name='main'),
    url(r'^main/$', wechat.main),

    url(r'^register/(?P<user_id>\d+)$', user.Register.as_view(), name='register'),
    url(r'^login/$', user.LoginView.as_view(), name='login'),
    url(r'^userinfo/$', user.UserInfoView.as_view(), name='userinfo'),

    url(r'^orderdetail/$', user.OrderDetailView.as_view(), name='orderdetail'),

    url(r'^bujiao/$', user.BuJiaoView.as_view(), name='bujiao'),
    url(r'^social/$', social.SocialView.as_view(), name='social'),

    url(r'^usertest/$', user.usertest)

]
