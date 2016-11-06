# coding: utf-8
from django.db import transaction
from django.utils import timezone
from datetime import datetime
from boai.apps.boai_model.models import AppSalesorderItems, AppSalesorders, AppSocials
from boai.libs.common.boai_enum import OrderStatus
from boai.libs.utility.serviceresult import ServiceResult, RuleViolation


class OrderService:
    def create_social_order(self, user_id, *args, **kwargs):
        result = ServiceResult()

        # user_id = kwargs.pop('user_id')
        social_base = kwargs.pop('social_base', 0)
        fund_base = kwargs.pop('fund_base', 0)
        social_type = kwargs.pop('social_type')
        is_social = kwargs.pop('is_social', False)
        is_fund = kwargs.pop('is_fund', False)

        social = AppSocials.objects.get(type=social_type, city='深圳')

        try:
            with transaction.atomic():
                order = AppSalesorders(user_id=user_id)
                order.order_id = datetime.now().strftime('%Y%m%d') + str(int(datetime.utcnow().timestamp()))
                order.orderstatus = 0
                order.createtime = timezone.now()

                order_item = AppSalesorderItems(order_id=order.order_id)
                order_item.user_id = user_id
                order_item.insured_city = '深圳'
                order_item.insured_type = social_type
                # 业务类型
                order_item.businesstype = 'social_fund'
                order_item.socialbase = social_base
                order_item.housingfundbase = fund_base

                order_item.startmonth = kwargs['startmonth']
                order_item.endmonth = kwargs['endmonth']

                if is_social:  # 社保费用
                    order_item.endowment = social_base * social.endowment
                    order_item.medical = social_base * social.medical
                    order_item.unemployment = social_base * social.unemployment
                    order_item.employment = social_base * social.employment
                    order_item.maternity = social_base * social.maternity
                    order_item.disability = social.disability
                if is_fund:  # 公积金费用
                    order_item.housingfund = fund_base * social.housingfund

                # 月数
                mon = order_item.endmonth.month - order_item.startmonth.month
                mon = mon if mon > 0 else 1

                # 社保、公积金费用
                social_amount = mon * (order_item.endowment + order_item.medical + order_item.unemployment +
                                       order_item.employment + order_item.maternity + order_item.disability + order_item.housingfund)
                # 手续费
                charge = 30 * mon + 10
                # 总费用
                total_amount = social_amount + charge

                order_item.mon = mon
                order_item.charge = charge
                order_item.totalamount = total_amount
                order.total_amount = total_amount
                order.discount_amount = 0
                order.pay_amount = total_amount
                order.save()
                order_item.save()
        except Exception as e:
            result.ruleviolations.append(RuleViolation('order', '保存失败'))
            return result
        return ServiceResult(order.order_id)
