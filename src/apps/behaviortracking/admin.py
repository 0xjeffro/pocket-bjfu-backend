from django.contrib import admin
from apps.users.models import UserProfile
from apps.behaviortracking.models import CaptureScreenTracking
from django.utils.html import format_html


# Register your models here.


class CaptureScreenTrackingAdmin(admin.ModelAdmin):
    list_display = ['c_user_info', 'pageUrl', 'options', 'createTime']
    search_fields = ['openId', 'options']
    list_filter = ['createTime', 'pageUrl']

    def c_user_info(self, obj):
        openId = obj.openId

        if openId == 'dev':
            return format_html(
                '<span style="display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3;overflow:'
                ' hidden;"">{}</span>',
                '开发者'
            )

        try:
            user = UserProfile.objects.get(openId=openId)
            info = user.realName + '（' + user.academy + user.xh[:2] + '）'
            return format_html(
                '<span style="display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3;overflow:'
                ' hidden;"">{}</span>',
                info
            )
        except Exception as e:
            return format_html(
                '<span style="display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3;overflow:'
                ' hidden;"">{}</span>',
                ''
            )

    c_user_info.short_description = '用户'


admin.site.register(CaptureScreenTracking, CaptureScreenTrackingAdmin)
