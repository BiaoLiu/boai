from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
from django.utils.html import format_html
from django.utils.translation import ugettext_lazy as _

from boai.apps.boai_admin.forms import BoaiUserChangeForm, BoaiUserCreationForm
from boai.apps.boai_model import models


# Register your models here.

# @admin.register(models.AuthUser)
# class UserAdmin(admin.ModelAdmin):
#     list_per_page = 15
#     list_display = ['id', 'mobile', 'email', 'date_joined', 'is_active']
#     list_display_links = ['id', 'mobile']
#     fields = ['username', 'mobile', 'nicknickname', 'realnickname', 'idcart', 'email', 'date_joined', 'is_active']
#
#     form = UserForm




class BoaiUserAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super(BoaiUserAdmin, self).__init__(*args, **kwargs)
        self.list_display = ('username', 'email', 'is_active', 'is_staff', 'is_superuser')
        self.search_fields = ('username', 'email', 'nickname')

        self.form = BoaiUserChangeForm  # 编辑用户表单
        self.add_form = BoaiUserCreationForm  # 添加用户表单

    def changelist_view(self, request, extra_context=None):
        # 这个方法在源码的admin/options.py文件的ModelAdmin这个类中定义，我们要重新定义它，以达到不同权限的用户，返回的表单内容不同

        self.fieldsets = ((None, {'fields': ('username', 'password',)}),
                          (_('Personal info'), {'fields': ('realname', 'mobile', 'idcart', 'email')}),
                          (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups')}),
                          (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
                          )
        self.add_fieldsets = ((None, {'classes': ('wide',),
                                      'fields': (
                                          'username', 'mobile', 'password1', 'password2', 'realname', 'idcart', 'email',
                                          'is_active',
                                          'is_staff', 'is_superuser', 'groups'),
                                      }),
                              )

        return super(BoaiUserAdmin, self).changelist_view(request, extra_context)

    def save_model(self, request, obj, form, change):
        realname = form.cleaned_data.get('realname')
        idcart = form.cleaned_data.get('idcart')
        obj.save()

        if not change:
            user_profile = models.AppUserProfile(user_id=obj.id)
        else:
            user_profile = form.instance.profile

        user_profile.realname = realname
        user_profile.idcart = idcart
        user_profile.save()


admin.site.register(models.AuthUser, BoaiUserAdmin)


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
    #     'fields': ('enable_comments', 'registration_required', 'template_nickname')
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
        return format_html('<a href="{0}">{1}</a>', url, realname)

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


@admin.register(models.AppCompany)
class AppAdmin(admin.ModelAdmin):
    class Media:
        js = (
            'js/kindeditor/kindeditor-all-min.js',
            'js/kindeditor/config.js'
        )
