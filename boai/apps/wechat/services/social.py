# coding:utf-8
from boai.apps.boai_model.models import AppSocialPrice
from boai.libs.utility.serviceresult import ServiceResult, RuleViolation


class SocialService:
    def get_social_price(self, social_type, city):
        result = ServiceResult()
        try:
            social = AppSocialPrice.objects.get(city=city, type=social_type)
        except AppSocialPrice.DoesNotExist:
            result.ruleviolations.append(RuleViolation('social', '社保数据不存在'))
            return result
        return ServiceResult(social)
