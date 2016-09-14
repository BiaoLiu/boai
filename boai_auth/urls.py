from django.conf.urls import url

from boai_auth.views import token_new, token

urlpatterns = [
    url(r'^get_token/$', token_new, name='api_token_new'),
    url(r'^token/(?P<token>.{24})/(?P<user>\d+).json$', token, name='api_token'),
]
