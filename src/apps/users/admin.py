from django.contrib import admin
from .models import UserProfile, BlackUser
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext, gettext_lazy as _

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin

# Register your models here.


class ProxyResource(resources.ModelResource):
    class Meta:
        model = UserProfile


class UserProfileAdmin(ImportExportActionModelAdmin):
    resource_class = ProxyResource
    ordering = ('-last_active',)
    list_display = ['realName', 'academy', 'xh', 'date_joined', 'last_active']
    list_filter = ['academy', 'verifyType']
    search_fields = ['realName', 'xh', 'academy', 'openId', ]
    list_per_page = 100
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('openId', 'realName', 'xh', 'pwd', 'verifyType', 'ksh', 'sfzh')}),
        (_('Permissions'), {
            'fields': ('is_staff', 'is_superuser', 'groups'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined', 'last_active')}),
    )


admin.site.register(UserProfile, UserProfileAdmin)


class BlackUserAdmin(admin.ModelAdmin):
    list_display = ['openId', 'xh']


admin.site.register(BlackUser, BlackUserAdmin)


admin.site.site_title = u"口袋北林后台管理系统"
admin.site.site_header = u"口袋北林后台管理系统"
