# coding: utf-8
from wechatpy import create_reply
from wechatpy.replies import TextReply

#from isay9685.models import CityWeahter

"""
微信事件处理
"""
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

"""
微信公众号关注
"""
def replySubscribe(msg):
    reply = TextReply(content='欢迎关注(博爱)BOAI的微信订阅号。', message=msg)
    return reply