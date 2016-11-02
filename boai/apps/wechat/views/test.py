# coding: utf-8
from django.http import HttpResponse


def test(request):
    xml = '<xml><return_code><![CDATA[{0}]]></return_code><return_msg><![CDATA[{1}]]></return_msg></xml>' \
        .format('200', 'OK')

    return HttpResponse(xml,content_type='text/xml')
