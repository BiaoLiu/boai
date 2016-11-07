from django.contrib import admin
from django.core.urlresolvers import reverse
from django.utils.html import format_html

from boai.apps.boai_model import models


# Register your models here.

@admin.register(models.AuthUser)
class UserAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'mobile', 'realname', 'email', 'date_joined', 'is_active']
    list_display_links = ['id', 'mobile', 'realname']

    def realname(self, instance):
        return instance.profile.realname

    realname.short_description = '姓名'


class SalesorderitemInline(admin.StackedInline):
    exclude = ['user_id', 'businesstype']
    model = models.AppSalesorderItems
    max_num = 1

    # fieldsets = (
    #     ('费用明细', {
    #         'classes': ('collapse',),
    #         'fields': ('insured_city', 'socialbase')
    #     }),
    # )

    # ('Advanced options', {
    #     'classes': ('collapse',),
    #     'fields': ('enable_comments', 'registration_required', 'template_name')
    # }),

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(models.AppSalesorders)
class SalesorderAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['order_id', 'user_link', 'total_amount', 'orderstatus', 'createtime', 'remark']
    inlines = [SalesorderitemInline]

    # fields = ['order_id','user']

    # readonly_fields = ['order_id', 'show_user']
    exclude = ['pay_amount']

    def user_link(self, instance):
        realname = instance.user.profile.realname
        url = ''
        return format_html("""<a href="{0}">{1}</a>""", url, realname)

    user_link.short_description = "用户"
    # 显示HTML
    user_link.allow_tags = True

    def has_add_permission(self, request):
        return False


@admin.register(models.AppSocials)
class SocialAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['id', 'city', 'type']
    list_display_links = ['id', 'city', 'type']
