from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from boai.apps.boai_model import models


# Register your models here.

@admin.register(models.AuthUser)
class UserAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'mobile', 'realname','email','date_joined', 'is_active']

    def realname(self, instance):
        return instance.profile.realname
    realname.short_description = '姓名'


@admin.register(models.AppSalesorders)
class SalesorderAdmin(admin.ModelAdmin):
    list_per_page = 15
    readonly_fields = ['order_id', 'show_url']
    list_display = ['order_id', 'user', 'total_amount', 'orderstatus', 'createtime', 'remark']
    readonly_fields = ['order_id', 'show_user']
    exclude = ['user_id', 'pay_amount']

    def show_user(self, instance):
        realname = instance.user_profile.realname
        url = ''
        return format_html("""<a href="{0}">{1}</a>""", url, realname)

    show_user.short_description = "用户"
    # 显示HTML
    show_user.allow_tags = True

    def has_add_permission(self, request):
        return False


@admin.register(models.AppSocials)
class SocialAdmin(admin.ModelAdmin):
    pass
