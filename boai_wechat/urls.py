from django.conf.urls import url
from boai_wechat.views import views as boai_wechat_views
urlpatterns = [
    url(r'^$', boai_wechat_views.index),
    url(r'^set_menu$', boai_wechat_views.create_menu),
]