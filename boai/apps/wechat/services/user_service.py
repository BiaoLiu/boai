# coding:utf-8
from boai.apps.boai_model.models import AppUserProfile, AuthUser


class UserService:
    def update_userinfo(self, user_id, *args, **kwargs):
        '''更新用户信息'''
        try:
            user = AuthUser.objects.get(id=user_id)
            user_profile = AppUserProfile.objects.get(user_id=user_id)
            user.email = kwargs.pop('email', '')
            user_profile.idcart = kwargs.pop('idcart', '')
            user_profile.social_city = kwargs.pop('social_city', '')
            user_profile.household_type = kwargs.pop('household_type', '')
            user_profile.cpf_account = kwargs.pop('cpf_count', '')
            user.save()
            user_profile.save()
        except(Exception) as e:
            return False
        return True
