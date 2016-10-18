from django.conf.urls import url

from .views import main as boai_wechat_views
from .views import main, user

urlpatterns = [
    # url(r'^$', boai_wechat_views.index),
    url(r'^set_menu$', boai_wechat_views.create_menu),

    url(r'^$', main.main, name='main'),

    url(r'^register/$', user.Register.as_view(), name='register'),

    url(r'^login/$', user.LoginView.as_view(), name='login'),

    url(r'^userinfo/$', user.UserInfoView.as_view(), name='userinfo'),

    url(r'^usertest/$', user.usertest)

]
