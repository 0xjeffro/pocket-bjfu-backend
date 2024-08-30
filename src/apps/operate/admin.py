from django.contrib import admin
from .models import LikeToComment, FavToContent, LikeToContent, ReportToContent
from apps.users.models import UserProfile
from apps.content.models import Content
from django.utils.html import format_html

# Register your models here.


class LikeToContentAdmin(admin.ModelAdmin):
    list_display = ['c_author_info', 'contentId', 'createTime']
    search_fields = ['openId', ]
    list_filter = ['createTime', ]
    list_per_page = 7

    def c_author_info(self, obj):
        openId = obj.openId

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
    c_author_info.short_description = '触发者'


admin.site.register(LikeToContent, LikeToContentAdmin)


class FavToContentAdmin(admin.ModelAdmin):
    list_display = ['c_author_info', 'contentId', 'createTime']
    search_fields = ['openId', ]
    list_filter = ['createTime', ]
    list_per_page = 7

    def c_author_info(self, obj):
        openId = obj.openId

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
    c_author_info.short_description = '触发者'


admin.site.register(FavToContent, FavToContentAdmin)


class LikeToCommentAdmin(admin.ModelAdmin):
    list_display = ['c_author_info', 'commentId', 'createTime']
    search_fields = ['openId', ]
    list_filter = ['createTime', ]
    list_per_page = 7

    def c_author_info(self, obj):
        openId = obj.openId

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
    c_author_info.short_description = '触发者'


admin.site.register(LikeToComment, LikeToCommentAdmin)


class ReportToContentAdmin(admin.ModelAdmin):
    list_display = ['c_report_user', 'c_reported_content', 'c_reported_user', 'createTime']
    search_fields = ['contentId', 'openId']
    list_filter = ['createTime', ]
    list_per_page = 7

    def c_report_user(self, obj):
        openId = obj.openId
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
    c_report_user.short_description = '举报人'

    def c_reported_content(self, obj):
        contentId = obj.contentId

        try:
            c = Content.objects.get(id=contentId)
            return format_html(
                '<span style="display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3;overflow:'
                ' hidden;"">{}</span>',
                c.contentText,
            )
        except Exception as e:
            return format_html(
                '<span style="display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3;overflow:'
                ' hidden;"">{}</span>',
                '内容不存在',
            )
    c_reported_content.short_description = '被举报内容'

    def c_reported_user(self, obj):
        contentId = obj.contentId

        try:
            c = Content.objects.get(id=contentId)
            user = UserProfile.objects.get(openId=c.openId)
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

    c_reported_user.short_description = '被举报用户'


admin.site.register(ReportToContent, ReportToContentAdmin)


