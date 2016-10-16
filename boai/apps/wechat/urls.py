from django.conf.urls import url

from .views import views as boai_wechat_views
from .views import views, user

urlpatterns = [
    # url(r'^$', boai_wechat_views.index),
    url(r'^set_menu$', boai_wechat_views.create_menu),

    url(r'^$', views.main, name='main'),

    url(r'^login/$', user.LoginView.as_view(), name='login'),

    url(r'^userinfo/$', user.UserInfoView.as_view(), name='userinfo'),

    url(r'^usertest/$', user.usertest)

]
