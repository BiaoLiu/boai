# coding:utf-8

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from wechatpy.pay import WeChatPay

from boai.apps.boai_model.models import AppSalesorders, AppPlatformUser


@login_required
def wechat_pay(request):
    user_id = request.user.id
    order_id = request.GET.get('orderid')

    try:
        order = AppSalesorders.objects.get(order_id=order_id, user_id=user_id)
    except AppSalesorders.DoesNotExist:
        return HttpResponse('订单不存在')

    platform_user = AppPlatformUser.objects.get(user_id=user_id)

    wechatpay = WeChatPay(settings.WECHAT_APP_ID, settings.WECHAT_KEY, settings.WECHAT_MCH_ID)
    # 统一下单
    unifiedorder_result = wechatpay.order.create('JSAPI', '商品名称', order.total_amount * 100, 'notify_url',
                                                 user_id=platform_user.openid,
                                                 out_trade_no=order.order_id)
    # 预支付订单id
    prepay_id = unifiedorder_result.get('prepay_id')

    paysign_params = wechatpay.jsapi.get_jsapi_params(prepay_id)

    return render(request, 'wechat/jsapi.html', paysign_params)


def paynotify_callback():
    pass
