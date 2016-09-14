# -*- coding: utf-8 -*-
from wechatpy import parse_message, create_reply
from wechatpy.replies import TextReply, ArticlesReply
from wechatpy.utils import check_signature
from wechatpy.exceptions import InvalidSignatureException

from boai_wechat.services.weatherservices import cityweather
# from isay9685.models import CityWeahter
import json
import time
from datetime import datetime


def doreply(msg):
    reply = None

    try:

        if msg.event == 'subscribe':
            reply = replySubscribe(msg)
        else:
            reply = create_reply(repr(msg), msg)

    except Exception as e:
        print('error:', e)
        reply = None

    return reply


def replySubscribe(msg):
    reply = TextReply(content='欢迎关注(博爱)BOAI的微信订阅号。', message=msg)
    return reply