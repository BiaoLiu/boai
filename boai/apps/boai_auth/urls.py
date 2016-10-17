from django.conf.urls import url

from .views import login, token, get_authcode

urlpatterns = [
    url(r'^login/$', login, name='api_token_new'),
    url(r'^get_authcode/$', get_authcode, name='api_authcode_new'),
    url(r'^token/(?P<token>.{24})/(?P<user>\d+).json$', token, name='api_token'),
]
