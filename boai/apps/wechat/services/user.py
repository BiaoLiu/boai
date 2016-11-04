# coding:utf-8
from boai.apps.boai_model.models import AppUserProfile, AuthUser


class UserService:
    def update_userinfo(self, user_id, *args, **kwargs):
        '''更新用户信息'''
        try:
            user = AuthUser.objects.get(id=user_id)
            user_profile = AppUserProfile.objects.get(user_id=user_id)
            user.email = kwargs['email']
            user_profile.realname = kwargs['realname']
            user_profile.idcart = kwargs['idcart']
            user_profile.social_city = kwargs['social_city']
            user_profile.household_type = kwargs['household_type']
            user_profile.cpf_account = kwargs['cpf_count']
            user.save()
            user_profile.save()
        except Exception as e:
            return False
        return True
