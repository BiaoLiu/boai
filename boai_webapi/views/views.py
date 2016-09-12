from django.http import HttpResponse

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