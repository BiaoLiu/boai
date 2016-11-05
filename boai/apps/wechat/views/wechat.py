# coding: utf-8
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from wechatpy import WeChatClient, parse_message, create_reply
from wechatpy.exceptions import InvalidSignatureException
from wechatpy.utils import check_signature
from wechatpy.replies import BaseReply, TextReply, ArticlesReply
from ..services.weather import cityweather
import json
import time


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
                "url": "http://m.91boai.com/wechat/wuxian/"
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
                        "url": "http://m.91boai.com/wechat/orderdetail/"
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
            reply = replySubscribe(msg)
        elif msg.event == 'click':
            if msg.key == 'BOAI_CONTACT_US':
                content = '尊敬的客户，您目前尚未分配专属客服！\n\n' \
                          '如有问题欢迎拨打91小保全国统一咨询热线：0755-83234691。\n' \
                          '91小保致力于提供个人客户更好的服务！'
                return TextReply(content=content, message=msg)
        else:
            reply = create_reply(repr(msg), msg)
    except Exception as e:
        print('error:', e)
    return reply


def replySubscribe(msg):
    '''
    微信公众号关注
    '''
    return TextReply(content='欢迎关注91小保！', message=msg)


def doreply_text(msg):
    '''
    微信文本消息处理
    '''
    reply = None
    try:
        if msg.content[-2:] == u'天气':
            if (len(msg.content) == 2):
                cityname = '合肥'
            else:
                cityname = msg.content[:-2]
            reply = replyWeather(cityname, msg)
        else:
            reply = create_reply(repr(msg), msg)
    except Exception as e:
        print('error:', e)
    return reply


def replyWeather(cityname, msg):
    reply = None
    dateid = time.strftime("%Y%m%d")
    timeid = time.strftime("%H")
    # cWeahter = CityWeahter.objects.filter(dateid=dateid, timeid=timeid, cityname=cityname)
    # if cWeahter:
    #     weatherstr = cWeahter[0].wheather
    # else:
    weatherstr = cityweather.getcityweather(cityname)
    #     cw = CityWeahter(dateid=dateid, timeid=timeid, cityname=cityname, wheather=weatherstr, createtime=datetime.now())
    #     cw.save()

    # weatherstr = '''{"error":0,"status":"success","date":"2015-06-15","results":[{"currentCity":"合肥","pm25":"126","index":[{"title":"穿衣","zs":"热","tipt":"穿衣指数","des":"天气热，建议着短裙、短裤、短薄外套、T恤等夏季服装。"},{"title":"洗车","zs":"不宜","tipt":"洗车指数","des":"不宜洗车，未来24小时内有雨，如果在此期间洗车，雨水和路上的泥水可能会再次弄脏您的爱车。"},{"title":"旅游","zs":"适宜","tipt":"旅游指数","des":"温度适宜，又有较弱降水和微风作伴，会给您的旅行带来意想不到的景象，适宜旅游，可不要错过机会呦！"},{"title":"感冒","zs":"较易发","tipt":"感冒指数","des":"相对今天出现了较大幅度降温，较易发生感冒，体质较弱的朋友请注意适当防护。"},{"title":"运动","zs":"较不宜","tipt":"运动指数","des":"有降水，推荐您在室内进行健身休闲运动；若坚持户外运动，须注意携带雨具并注意避雨防滑。"},{"title":"紫外线强度","zs":"弱","tipt":"紫外线强度指数","des":"紫外线强度较弱，建议出门前涂擦SPF在12-15之间、PA+的防晒护肤品。"}],"weather_data":[{"date":"周一 06月15日 (实时：27℃)","dayPictureUrl":"http://api.map.baidu.com/images/weather/day/xiaoyu.png","nightPictureUrl":"http://api.map.baidu.com/images/weather/night/zhongyu.png","weather":"小雨转中雨","wind":"南风微风","temperature":"28 ~ 22℃"},{"date":"周二","dayPictureUrl":"http://api.map.baidu.com/images/weather/day/dayu.png","nightPictureUrl":"http://api.map.baidu.com/images/weather/night/xiaoyu.png","weather":"大雨转小雨","wind":"北风微风","temperature":"26 ~ 21℃"},{"date":"周三","dayPictureUrl":"http://api.map.baidu.com/images/weather/day/xiaoyu.png","nightPictureUrl":"http://api.map.baidu.com/images/weather/night/yin.png","weather":"小雨转阴","wind":"北风微风","temperature":"24 ~ 20℃"},{"date":"周四","dayPictureUrl":"http://api.map.baidu.com/images/weather/day/duoyun.png","nightPictureUrl":"http://api.map.baidu.com/images/weather/night/duoyun.png","weather":"多云","wind":"东北风3-4级","temperature":"28 ~ 20℃"}]}]} '''
    weatherjson = json.loads(weatherstr)

    if weatherjson and weatherjson.get('error') == 0:
        date = weatherjson.get('date')
        result = weatherjson.get('results')[0]
        currentCity = result.get('currentCity')
        pm25 = result.get('pm25')
        wheathernowdatas = result.get('weather_data')[0]
        weathermsg = repr(wheathernowdatas)
        reply = ArticlesReply(message=msg)
        # simply use dict as article
        reply.add_article({
            'title': wheathernowdatas.get('date'),
        })
        reply.add_article({
            'title':
                u'%s %s %s' % (
                    wheathernowdatas.get('weather'), wheathernowdatas.get('temperature'), wheathernowdatas.get('wind')) \
                + '\r\n' \
                + '\r\n' \
                + currentCity + u' PM2.5: ' + pm25,
            'url': 'http://blog.popyelove.com'
        })
        reply.add_article({
            'title': u'白天',
            'image': wheathernowdatas.get('dayPictureUrl'),
        })
        reply.add_article({
            'title': u'晚上',
            'image': wheathernowdatas.get('nightPictureUrl'),
        })
    return reply
