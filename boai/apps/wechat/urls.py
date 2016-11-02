from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .views import wechat, wechatpay, user, social, order, test

router = DefaultRouter()
router.register('social', social.SocialViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^$', wechat.main, name='main'),
    url(r'^main/$', wechat.main),
    url(r'^set_menu$', wechat.create_menu),
    url(r'^getauth/$', wechat.get_auth),
    url(r'^getauthcallback/$', wechat.get_auth_callback),

    url(r'^pay/$', wechatpay.pay),
    url(r'^paynotify/$', wechatpay.paynotify),

    url(r'^register/(?P<user_id>\d+)$', user.Register.as_view(), name='register'),
    url(r'^login/$', user.LoginView.as_view(), name='login'),
    url(r'^userinfo/$', user.UserInfoView.as_view(), name='userinfo'),

    # url(r'^social/$', social.SocialView.as_view(), name='social'),
    url(r'^wuxian/$', social.SocialView.as_view(), name='social'),
    url(r'^bujiao/$', social.BuJiaoView.as_view(), name='bujiao'),

    url(r'^orderdetail/$', order.OrderDetailView.as_view(), name='orderdetail'),

    url(r'^usertest/$', user.usertest),

    url(r'^test/', test.test),

]
