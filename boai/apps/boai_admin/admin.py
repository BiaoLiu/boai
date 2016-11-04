from django.contrib import admin

from boai.apps.boai_model import models


# Register your models here.

@admin.register(models.AppSalesorders)
class SalesorderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.AppSocials)
class SocialAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.AuthUser)
