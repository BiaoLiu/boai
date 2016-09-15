from django.conf.urls import url

from boai_auth.views import token_new, token, get_authcode

urlpatterns = [
    url(r'^get_token/$', token_new, name='api_token_new'),
    url(r'^get_authcode/$', get_authcode, name='api_authcode_new'),
    url(r'^token/(?P<token>.{24})/(?P<user>\d+).json$', token, name='api_token'),
]
