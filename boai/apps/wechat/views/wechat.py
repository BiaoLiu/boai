# coding: utf-8
import uuid

from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import transaction
from django.http import HttpResponse
from django.contrib import auth
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from datetime import datetime, timedelta
from wechatpy import WeChatClient
from wechatpy import parse_message, create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import BaseReply
from wechatpy.utils import check_signature
from wechatpy.oauth import WeChatOAuth
from boai.apps.boai_model.models import AppUserProfile, AuthUser, AppPlatformUser
from . import wechat_reply_event
from . import wechat_reply_text


def main(request):
    '''主页'''
    return HttpResponse('welcome to 91小保')


"""
微信服务器授权
"""


@csrf_exempt
def index(request):
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        try:
            check_signature(settings.WECHAT_APP_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = 'error'
        response = HttpResponse(echo_str, content_type="text/plain")
        return response
    else:
        reply = None
        msg = parse_message(request.body)
        if msg.type == 'text':
            reply = wechat_reply_text.doreply(msg)
        elif msg.type == 'event':
            reply = wechat_reply_event.doreply(msg)
        else:
            pass
        if not reply or not isinstance(reply, BaseReply):
            reply = create_reply('程序猿哥哥正在开发中', msg)
        response = HttpResponse(reply.render(), content_type="application/xml")
        return response


"""
weiixn
"""


@csrf_exempt
def create_menu(request):
    client = WeChatClient(settings.WECHAT_APP_ID, settings.WECHAT_APP_SECRET)
    menures = client.menu.create({
        "button": [
            {
                "name": "业务办理",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "五险一金",
                        "url": "http://blog.popyelove.com"
                    },
                    {
                        "type": "view",
                        "name": "补缴",
                        "url": "http://blog.popyelove.com"
                    }
                ]
            },
            {
                "name": "实用工具",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "社保计算器",
                        "url": "http://blog.popyelove.com"
                    }
                ]
            },
            {
                "name": "个人帐户",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "基本信息",
                        "url": "http://blog.popyelove.com"
                    },
                    {
                        "type": "view",
                        "name": "帐户余额",
                        "url": "http://blog.popyelove.com"
                    },
                    {
                        "type": "view",
                        "name": "帐户详情",
                        "url": "http://blog.popyelove.com"
                    },
                    {
                        "type": "view",
                        "name": "订单进展",
                        "url": "http://blog.popyelove.com"
                    },
                    {
                        "type": "click",
                        "name": "联系我们",
                        "key": "BOAI_CONTACT_US"
                    }
                ]
            }
        ]
    })
    if menures and menures.get('errcode') == 0:
        return HttpResponse('菜单设置成功')
    else:
        return HttpResponse('菜单设置失败')


@require_GET
def get_auth(request):
    '''获取微信授权'''
    back_url = 'http://' + request.get_host() + '/wechat/auth_callback/'
    next_url = request.GET.get('next', '')
    oauth = WeChatOAuth(settings.WECHAT_APP_ID, settings.WECHAT_APP_SECRET, back_url,
                        scope='snsapi_userinfo', state=next_url)
    return redirect(to=oauth.authorize_url)


@require_GET
def auth_callback(request):
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
                AppUserProfile.objects.create(user_id=user.id)
                # 保存微信授权信息
                platform_user = AppPlatformUser(user_id=user.id, nickname=user.nickname, avatar=user.avatar,
                                                platform='wechat')
                platform_user.openid = oauth.open_id
                platform_user.access_token = oauth.access_token
                platform_user.refresh_token = oauth.refresh_token
                platform_user.expiretime = datetime.utcnow() + timedelta(seconds=7200)
                platform_user.save()
        except (Exception) as e:
            pass
    else:
        user = AuthUser.objects.get(id=platform_user.user_id)
        if user.username and user.mobile and user.password:
            # 更新token
            platform_user.access_token = oauth.access_token
            platform_user.refresh_token = oauth.refresh_token
            platform_user.expiretime = datetime.utcnow() + timedelta(seconds=7200)
            platform_user.save()
            # 登录
            auth.login(request, auth.authenticate(username=user.mobile))
            return redirect(next_url if next_url else 'wechat:main')

    # 跳转至 完善注册页
    auth.login(request, auth.authenticate(username=user.username))
    return redirect('wechat:register', **{'user_id': user.id})
