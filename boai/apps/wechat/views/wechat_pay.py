# coding:utf-8
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone
from wechatpy.pay import WeChatPay
from wechatpy.exceptions import InvalidSignatureException

from boai.apps.boai_model.models import AppSalesorders, AppPlatformUser
from boai.libs.common.boai_enum import OrderStatus


@login_required
def pay(request):
    '''
    微信支付
    '''
    user_id = request.user.id
    order_id = request.GET.get('order_id')

    try:
        order = AppSalesorders.objects.get(order_id=order_id, user_id=user_id, orderstatus=OrderStatus.UnPaid.value)
    except AppSalesorders.DoesNotExist:
        return HttpResponse('订单不存在')

    platform_user = AppPlatformUser.objects.get(user_id=user_id)

    wechatpay = WeChatPay(settings.WECHAT_APP_ID, settings.WECHAT_KEY, settings.WECHAT_MCH_ID)
    # 统一下单
    unifiedorder_result = wechatpay.order.create('JSAPI', '社保公积金', str(int(order.pay_amount * 100)),
                                                 settings.SITE_DOMAIN + 'wechat/paynotify/',
                                                 user_id=platform_user.openid,
                                                 out_trade_no=order_id)
    # 预支付订单号
    prepay_id = unifiedorder_result.get('prepay_id')
    # 获取 JSAPI 参数
    paysign_params = wechatpay.jsapi.get_jsapi_params(prepay_id)

    return render(request, 'wechat/jsapi.html', paysign_params)


def paynotify(request):
    '''
    微信支付异步回调
    '''
    data = request.body.decode('utf-8')

    try:
        wechatpay = WeChatPay(settings.WECHAT_APP_ID, settings.WECHAT_KEY, settings.WECHAT_MCH_ID)
        data = wechatpay.parse_payment_result(data)
    except InvalidSignatureException:
        print('微信支付异步回调签名错误')

    return_code = data.get('return_code')
    return_msg = data.get('return_msg')
    out_trade_no = data.get('out_trade_no')
    transaction_id = data.get('transaction_id')

    if (return_code == 'SUCCESS'):
        orders = AppSalesorders.objects.filter(order_id=out_trade_no, orderstatus=OrderStatus.UnPaid.value)
        if orders:
            # 订单处理
            order = orders[0]
            order.transaction_id = transaction_id
            order.orderstatus = OrderStatus.Paid.value
            order.clientsource = 'wechat'
            order.paytype = 'wechat'
            order.paytime = timezone.now()
            order.save()

    xml = '<xml><return_code><![CDATA[{0}]]></return_code><return_msg><![CDATA[{1}]]></return_msg></xml>' \
        .format(return_code, 'OK')

    return HttpResponse(xml, content_type='text/xml')
