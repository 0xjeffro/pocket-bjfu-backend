from django.contrib import admin
from .models import Comment
from apps.users.models import UserProfile
from django.utils.html import format_html

# Register your models here.

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin


class ProxyResource(resources.ModelResource):
    class Meta:
        model = Comment


class CommentModelsAdmin(ImportExportActionModelAdmin):
    list_display = ['id', 'c_comment_abstract', 'c_author_info', 'nLike', 'createTime', 'state', 'deep', 'contentId',
                    'commentId']
    fields_options = {
        'c_comment_abstract': {
            'width': '400px',
        },
        'c_author_info': {
            'width': '250px'
        },
        'nLike': {
            'width': '110px'
        },
        'createTime': {
            'width': '170px'
        },
        'state': {
            'width': '110px'
        },
        'deep': {
            'width': '120px'
        },
        'contentId': {
            'width': '160px'
        },
        'commentId': {
            'width': '160px'
        }
    }
    list_filter = ['createTime', ]
    search_fields = ['id', 'commentText', 'openId']
    list_per_page = 100

    def c_comment_abstract(self, obj):

        return format_html(
            '<span style="display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3;overflow:'
            ' hidden;"">{}</span>',
            obj.commentText,
        )
    c_comment_abstract.short_description = '内容'

    def c_author_info(self, obj):
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

    c_author_info.short_description = '作者'


admin.site.register(Comment, CommentModelsAdmin)
