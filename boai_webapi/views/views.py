from django.http import HttpResponse

# Create your views here.
from django.views.generic import ListView
from boai_auth.decorators import token_required
from boai_webapi.services.sms_service import SmsService
from boai_model.models import AppUserProfile


class ApiEndpoint(ListView):
    @token_required
    def post(self, request, *args, **kwargs):
        return HttpResponse('Hello, OAuth2!')

def test(request):
    result = SmsService.send_code('18665937537')
    return HttpResponse('Hello test')