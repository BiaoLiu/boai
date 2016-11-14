# coding: utf-8
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from django.utils import timezone
from datetime import timedelta
from wechatpy.oauth import WeChatOAuth
from boai.apps.boai_model.models import AppUserProfile, AuthUser, AppPlatformUser
import uuid


@require_GET
def get_auth(request):
    '''获取微信授权'''
    back_url = 'http://' + request.get_host() + '/wechat/getauthcallback/'
    next_url = request.GET.get('next', '')
    oauth = WeChatOAuth(settings.WECHAT_APP_ID, settings.WECHAT_APP_SECRET, back_url,
                        scope='snsapi_userinfo', state=next_url)
    return redirect(to=oauth.authorize_url)


@require_GET
def get_auth_callback(request):
    '''微信授权回调'''
    code = request.GET.get('code')
    next_url = request.GET.get('state')

    if not code:
        return HttpResponse('您拒绝了授权！')

    oauth = WeChatOAuth(settings.WECHAT_APP_ID, settings.WECHAT_APP_SECRET, '')
    # 通过code换取access_token
    try:
        oauth.fetch_access_token(code)
    except Exception as e:
        return HttpResponse('获取微信授权出错！')

    try:
        platform_user = AppPlatformUser.objects.get(openid=oauth.open_id)
    except AppPlatformUser.DoesNotExist:
        try:
            with transaction.atomic():  # 启用事务提交
                # 获取微信用户信息
                res = oauth.get_user_info()
                # 创建用户
                user = AuthUser(password='')
                user.username = '91boai' + str(uuid.uuid1()).replace('-', '')[:20]
                user.nickname = res['nickname']
                user.avatar = res['headimgurl']
                user.save()
                # 保存user profile
                user_profile = AppUserProfile(user_id=user.id)
                user_profile.save()
                # 保存微信授权信息
                platform_user = AppPlatformUser(user_id=user.id, nickname=user.nickname, avatar=user.avatar,
                                                platform='wechat')
                platform_user.openid = oauth.open_id
                platform_user.access_token = oauth.access_token
                platform_user.refresh_token = oauth.refresh_token
                platform_user.expiretime = timezone.now() + timedelta(seconds=7200)
                platform_user.save()
        except (Exception) as e:
            return HttpResponse('微信登录出错!')
        else:
            request.session['user_id'] = user.id
            # 跳转至 完善注册页
            # return redirect('wechat:register', **{'user_id': user.id})
            return redirect('/wechat/register/{0}/?next={1}'.format(user.id, next_url))
    else:
        user = AuthUser.objects.get(id=platform_user.user_id)
        if user.username and user.mobile and user.password:
            # 更新token
            platform_user.access_token = oauth.access_token
            platform_user.refresh_token = oauth.refresh_token
            platform_user.expiretime = timezone.now() + timedelta(seconds=7200)
            platform_user.save()
            # 登录
            auth.login(request, auth.authenticate(username=user.mobile))
        # 跳转至主页
        return redirect(next_url if next_url else 'wechat:main')
