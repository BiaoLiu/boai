from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class AuthUser(AbstractUser):
    mobile = models.CharField('手机', max_length=20, null=True)
    avatar = models.CharField('头像', max_length=200, default='')

    class Meta:
        db_table='auth_user'


class AppStock(models.Model):
    pk_stock = models.CharField('股票代码', primary_key=True, max_length=40)
    stockname = models.CharField(u'股票名称', max_length=100, blank=True, null=True)
    tradetype = models.CharField('股票类型', max_length=100, blank=True, null=True)
    isdisabled = models.NullBooleanField('是否启用', blank=True, null=True)
    istop = models.NullBooleanField('是否置顶', blank=True, null=True)
    sortno = models.IntegerField('排序号', blank=True, null=True)
    createtime = models.DateTimeField('创建时间', auto_now_add=True, blank=True, null=True)

    class Meta:
        db_table = 'app_stock'
        verbose_name = '股票'
        verbose_name_plural = '股票列表'

    def __str__(self):
        return self.pk_stock + ':' + self.stockname