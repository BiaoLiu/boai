# coding: utf-8
from django.http import HttpResponse
from django.shortcuts import redirect


def test(request):
    xml = '<xml><return_code><![CDATA[{0}]]></return_code><return_msg><![CDATA[{1}]]></return_msg></xml>' \
        .format('200', 'OK')

    request.session['user_id']=1

    return redirect('/wechat/register/1/?next=/wechat/main/')

    # return HttpResponse(xml,content_type='text/xml')
