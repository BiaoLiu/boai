from boai.apps.boai_model.models import AppSendsms, AuthUser
from django.conf import settings
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt

from boai.apps.webapi.services.sms_service import SmsService
from boai.libs.common.response import res_msg
from .http import JsonResponseForbidden, JsonResponse, JsonResponseUnauthorized, JsonError
from .tokens import token_generator

try:
    from django.contrib.auth import get_user_model
except ImportError:  # Django < 1.5
    from django.contrib.auth.models import User
else:
    User = get_user_model()


# Creates a token if the correct username and password is given
# token/new.json
# Required: username&password
# Returns: success&token&user_id
@csrf_exempt
def login(request):
    '''登录'''
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        mobile = request.POST.get('mobile')
        auth_code = request.POST.get('auth_code')

        user = ''
        # 用户名、密码登录
        if username and password:
            user = authenticate(username=username, password=password)
        # 手机号码登陆
        elif mobile and auth_code:
            try:
                sms = AppSendsms.objects.filter(mobile=mobile).order_by('-createtime')[0]
                if sms.captcha == auth_code:
                    user = AuthUser.objects.get(mobile=mobile)
            except (AppSendsms.DoesNotExist, AuthUser.DoesNotExist):
                return JsonError("User does not exist.")
        else:
            return JsonError("Must include 'username' and 'password' as POST parameters.")

        if user:
            TOKEN_CHECK_ACTIVE_USER = getattr(settings, "TOKEN_CHECK_ACTIVE_USER", False)

            if TOKEN_CHECK_ACTIVE_USER and not user.is_active:
                return JsonResponseForbidden("User account is disabled.")

            res_msg['data'] = {
                'user_id': user.pk,
                'token': token_generator.make_token(user),
                'expire_time': ''
            }

            return JsonResponse(res_msg)
        else:
            return JsonResponseUnauthorized("Unable to log you in, please try again.")

    else:
        return JsonError("Must access via a POST request.")


@csrf_exempt
def get_authcode(request):
    '''获取手机验证码'''
    if request.method == 'POST':
        mobile = request.POST.get('mobile')

        if mobile:
            res_msg['data'] = SmsService.send_code(mobile)
            return JsonResponse(res_msg)
        else:
            return JsonError('mobile is required.')
    else:
        return JsonError("Must access via a POST request.")



# Checks if a given token and user pair is valid
# token/:token/:user.json
# Required: user
# Returns: success
def token(request, token, user):
    try:
        user = User.objects.get(pk=user)
    except User.DoesNotExist:
        return JsonError("User does not exist.")

    TOKEN_CHECK_ACTIVE_USER = getattr(settings, "TOKEN_CHECK_ACTIVE_USER", False)

    if TOKEN_CHECK_ACTIVE_USER and not user.is_active:
        return JsonError("User account is disabled.")

    if token_generator.check_token(user, token):
        return JsonResponse({})
    else:
        return JsonError("Token did not match user.")
