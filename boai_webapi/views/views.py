from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from oauth2_provider.views import ProtectedResourceView


class ApiEndpoint(ProtectedResourceView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')