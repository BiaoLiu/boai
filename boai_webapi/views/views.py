from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
# from oauth2_provider.views import ProtectedResourceView


class ApiEndpoint(ListView):
    def get(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')



class BoaiBackend:
    def authenticate(self,username,password):
        if username=='lbi':
            user=User.objects.get(username=username)
            return user
        return None

    def get_user(self,user_id):
        pass


class TokenBackend(ModelBackend):
    def authenticate(self, pk, token = None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return None
        if default_token_generator.check_token(user, token):
            return user
        return None