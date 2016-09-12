from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView
from tokenapi.decorators import token_required



class ApiEndpoint(ListView):
    @token_required
    def post(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')

@token_required
def test(request):
    if request.method=='POST':
        return HttpResponse('Hello test')