from django.http import HttpResponse
from django.template import RequestContext, Template
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str

from wechatpy import parse_message, create_reply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.replies import BaseReply

from boai_wechat.views import reply_text
from boai_wechat.views import reply_event

TOKEN = 'weixin'  # 注意要与微信公众帐号平台上填写一致


@csrf_exempt
def index(request):
    if request.method == 'GET':
        signature = request.GET.get('signature', '')
        timestamp = request.GET.get('timestamp', '')
        nonce = request.GET.get('nonce', '')
        echo_str = request.GET.get('echostr', '')
        try:
            check_signature(TOKEN, signature, timestamp, nonce)
        except InvalidSignatureException:
            echo_str = 'error'
        response = HttpResponse(echo_str, content_type="text/plain")
        return response
    else:
        reply = None
        msg = parse_message(request.body)
        if msg.type == 'text':
            reply = reply_text.doreply(msg)
        elif msg.type == 'event':
            reply = reply_event.doreply(msg)
        else:
            pass

        if not reply or not isinstance(reply, BaseReply):
            reply = create_reply('程序猿哥哥正在开发中', msg)

        response = HttpResponse(reply.render(), content_type="application/xml")
        return response