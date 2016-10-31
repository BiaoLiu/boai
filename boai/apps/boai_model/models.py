from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from boai.libs.common.string_extension import get_uuid


class AuthUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        '''创建user'''
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=AuthUserManager.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)

        # 添加用户详细信息
        user_profile = AppUserProfile(user_id=user.id)
        user_profile.save()

        return user

    def create_superuser(self, email, username, password):
        '''创建超级管理员'''
        user = self.create_user(email,
                                username=username,
                                password=password,
                                )

        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class AuthUser(AbstractUser):
    nickname = models.CharField('昵称', max_length=40, blank=True, null=True)
    mobile = models.CharField('手机', max_length=20, null=True)
    avatar = models.CharField('头像', max_length=200, default='')
    is_enterprise = models.NullBooleanField('是否企业用户')

    def __init__(self, *args, **kwargs):
        self._user_profile = None
        super(AuthUser, self).__init__(*args, **kwargs)

    objects = AuthUserManager()

    class Meta:
        db_table = 'auth_user'

    @property
    def profile(self):
        if self._user_profile: return self._user_profile
        try:
            self._user_profile = AppUserProfile.objects.get(user_id=self.id)
        except AppUserProfile.DoesNotExist:
            return None
        return self._user_profile


class AppUserProfile(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    puser_id = models.IntegerField('所属用户', blank=True, null=True)
    realname = models.CharField(max_length=20, blank=True, null=True)
    idcart = models.CharField(max_length=20, blank=True, null=True)
    social_province = models.CharField(max_length=20, blank=True, null=True)
    social_city = models.CharField(max_length=20, blank=True, null=True)
    idcart_front = models.CharField(max_length=200, blank=True, null=True)
    idcart_back = models.CharField(max_length=200, blank=True, null=True)
    household_type = models.CharField(max_length=20, blank=True, null=True)
    cpf_account = models.CharField(max_length=20, blank=True, null=True)
    bank_account = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        db_table = 'app_user_profile'


class AppPlatformUser(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    nickname = models.CharField(max_length=40, blank=True, null=True)
    avatar = models.CharField(max_length=200, blank=True, null=True)
    platform = models.CharField(max_length=20, blank=True, null=True)
    openid = models.CharField(max_length=200, blank=True, null=True)
    unionid = models.CharField(max_length=200, blank=True, null=True)
    access_token = models.CharField(max_length=200, blank=True, null=True)
    refresh_token = models.CharField(max_length=200, blank=True, null=True)
    expiretime = models.DateTimeField(blank=True, null=True)
    profileurl = models.CharField(max_length=200, blank=True, null=True)
    ts = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        db_table = 'app_platform_user'


class AppCompany(models.Model):
    user_id = models.IntegerField(blank=True, null=True)
    companyname = models.CharField(max_length=200, blank=True, null=True)
    province = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    people_num = models.IntegerField(blank=True, null=True)
    remark = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'app_company'


class AppSendsms(models.Model):
    sms_id = models.CharField(primary_key=True, max_length=40, default=get_uuid())
    mobile = models.CharField(max_length=20, blank=True, null=True)
    content = models.CharField(max_length=500, blank=True, null=True)
    captcha = models.CharField(max_length=20, blank=True, null=True)
    device_id = models.CharField(max_length=20, blank=True, null=True)
    is_success = models.NullBooleanField(blank=True, null=True)
    createtime = models.DateTimeField(blank=True, null=True, auto_now_add=True)

    class Meta:
        db_table = 'app_sendsms'


class AppSalesorderItems(models.Model):
    order_id = models.CharField(max_length=40, blank=True, null=True)
    user_id = models.IntegerField(blank=True, null=True)
    insured_city = models.CharField(max_length=20, blank=True, null=True)
    insured_type = models.CharField(max_length=20, blank=True, null=True)
    businesstype = models.CharField(max_length=40, blank=True, null=True)
    socialbase = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    housingfundbase = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    endowment = models.DecimalField(max_digits=18, decimal_places=2, default=0, blank=True, null=True)
    medical = models.DecimalField(max_digits=18, decimal_places=2, default=0, blank=True, null=True)
    unemployment = models.DecimalField(max_digits=18, decimal_places=2, default=0, blank=True, null=True)
    employment = models.DecimalField(max_digits=18, decimal_places=2, default=0, blank=True, null=True)
    maternity = models.DecimalField(max_digits=18, decimal_places=2, default=0, blank=True, null=True)
    disability = models.DecimalField(max_digits=18, decimal_places=2, default=0, blank=True, null=True)
    housingfund = models.DecimalField(max_digits=18, decimal_places=2, default=0, blank=True, null=True)
    startmonth = models.DateTimeField(blank=True, null=True)
    endmonth = models.DateTimeField(blank=True, null=True)
    # fund_startmonth = models.DateTimeField(blank=True, null=True)
    # fund_endmonth = models.DateTimeField(blank=True, null=True)
    mon = models.IntegerField(blank=True, null=True)
    charge = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    totalamount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'app_salesorder_items'


class AppSalesorders(models.Model):
    order_id = models.CharField(primary_key=True, max_length=40)
    user_id = models.IntegerField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    discount_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    pay_amount = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    paytype = models.CharField(max_length=20, blank=True, null=True)
    clientsource = models.CharField(max_length=20, blank=True, null=True)
    orderstatus = models.IntegerField(blank=True, null=True)
    createtime = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    paytime = models.DateTimeField(blank=True, null=True)
    remark = models.CharField(max_length=500, blank=True, null=True)

    class Meta:
        db_table = 'app_salesorders'


class AppSocials(models.Model):
    city = models.CharField(max_length=20, blank=True, null=True)
    type = models.CharField(max_length=20, blank=True, null=True)
    socialbase_min = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    socialbase_max = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    housingfundbase_min = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    housingfundbase_max = models.DecimalField(max_digits=18, decimal_places=2, blank=True, null=True)
    endowment = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    medical = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    unemployment = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    employment = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    maternity = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    disability = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)
    housingfund = models.DecimalField(max_digits=18, decimal_places=4, blank=True, null=True)

    class Meta:
        db_table = 'app_socials'
