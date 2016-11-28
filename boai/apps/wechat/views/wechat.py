# coding: utf-8
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechatpy import WeChatClient, parse_message, create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature
from wechatpy.replies import BaseReply, TextReply


def main(request):
    '''主页'''
    return HttpResponse('welcome to 91小保')


@csrf_exempt
def index(request):
    '''
    微信服务器授权
    '''
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        try:
            check_signature(settings.WECHAT_APP_TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = 'error'
        return HttpResponse(echo_str, content_type="text/plain")
    else:
        reply = None
        msg = parse_message(request.body)
        if msg.type == 'text':  # 文本消息
            reply = doreply_text(msg)
        elif msg.type == 'event':  # 事件消息
            reply = doreply_event(msg)

        if not reply or not isinstance(reply, BaseReply):
            reply = create_reply('程序猿哥哥正在开发中', msg)
        return HttpResponse(reply.render(), content_type="application/xml")


@csrf_exempt
def create_menu(request):
    '''
    创建自定义菜单
    '''
    client = WeChatClient(settings.WECHAT_APP_ID, settings.WECHAT_APP_SECRET)
    menures = client.menu.create({
        "button": [
            {
                "type": "click",
                "name": "关于我们",
                "key": "BOAI_CONTACT_US"
            },
            {
                "type": "view",
                "name": "社保缴纳",
                "url": "http://m.91boai.com/wechat/social/"
            },
            {
                "name": "个人帐户",
                "sub_button": [
                    {
                        "type": "view",
                        "name": "基本信息",
                        "url": "http://m.91boai.com/wechat/userinfo/"
                    },
                    {
                        "type": "view",
                        "name": "我的订单",
                        "url": "http://m.91boai.com/wechat/unpayorder/"
                    }
                ]
            }
        ]
    })
    if menures and menures.get('errcode') == 0:
        return HttpResponse('菜单设置成功')
    else:
        return HttpResponse('菜单设置失败')


def doreply_event(msg):
    '''
    微信事件处理
    '''
    reply = None
    try:
        if msg.event == 'subscribe':
            reply = reply_subscribe(msg)
        elif msg.event == 'click':
            if msg.key == 'BOAI_CONTACT_US':
                content = '尊敬的客户，您目前尚未分配专属客服！\n\n' \
                          '如有问题欢迎拨打91小保全国统一咨询热线：0755-83234691。\n' \
                          '91小保致力于提供个人客户更好的服务！'
                return TextReply(content=content, message=msg)
        else:
            reply = create_reply('详细咨询请拨打91小保全国统一咨询热线：0755-83234691。', msg)
    except Exception as e:
        print('error:', e)
    return reply


def reply_subscribe(msg):
    '''
    微信公众号关注
    '''
    return TextReply(content='欢迎关注91小保！', message=msg)


def doreply_text(msg):
    '''
    微信文本消息处理
    '''
    return create_reply('详细咨询请拨打91小保全国统一咨询热线：0755-83234691。', msg)
