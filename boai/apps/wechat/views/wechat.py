# coding: utf-8
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from wechatpy import WeChatClient
from wechatpy import parse_message, create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import BaseReply
from wechatpy.utils import check_signature
from wechatpy.oauth import WeChatOAuth

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


def test(request):
    back_url = '/wechat/jsapi_code/'
    WeChatOAuth(settings.WECHAT_APP_ID, settings.WECHAT_APP_SECRET, back_url)


@require_GET
def jsapi_code(request):
    code = request.GET.get('code')
    state = request.GET.get('state')

    if not code:
        return HttpResponse('您拒绝了授权！')

    oauth = WeChatOAuth(settings.WECHAT_APP_ID, settings.WECHAT_APP_SECRET, '')
    # 通过code换取access_token
    oauth.fetch_access_token(code)

    oauth.access_token

    return HttpResponse('jsapi_code')
