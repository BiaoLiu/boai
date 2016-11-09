from django.conf.urls import url, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from .views import wechat, wechat_login, wechat_pay, user, social, order, test

router = DefaultRouter()
router.register('social', social.SocialViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
    url(r'^$', wechat.main, name='main'),
    url(r'^main/$', wechat.main),
    url(r'^index/', wechat.index),
    url(r'^setmenu/$', wechat.create_menu),

    url(r'^getauth/$', wechat_login.get_auth),
    url(r'^getauthcallback/$', wechat_login.get_auth_callback),

    url(r'^pay/$', wechat_pay.pay),
    url(r'^paynotify/$', wechat_pay.paynotify),

    url(r'^register/(?P<user_id>\d+)/$', user.Register.as_view(), name='register'),
    url(r'^login/$', user.LoginView.as_view(), name='login'),
    url(r'^userinfo/$', user.UserInfoView.as_view(), name='userinfo'),

    url(r'^wuxian/$', social.SocialView.as_view(), name='social'),

    url(r'^payorder/$', order.PayOrderView.as_view(), name='payorder'),
    url(r'^payed_detail/(?P<order_id>\w+)$', order.PayOrderDetailView.as_view(), name='payorder_detail'),
    url(r'^unpayorder/$', order.UnPayOrderView.as_view(), name='unpayorder'),
    url(r'^unpayorder/(?P<order_id>\w+)$', order.UnPayOrderDetailView.as_view(), name='unpayorder_detail'),

    url(r'^usertest/$', user.usertest),

    url(r'^test/', test.test),

]
