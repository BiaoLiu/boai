from django.conf.urls import url

from tokenapi.views import token
from tokenapi.views import token_new


urlpatterns = [
    url(r'^get_token/$', token_new, name='api_token_new'),
    url(r'^token/(?P<token>.{24})/(?P<user>\d+).json$', token, name='api_token'),
]
