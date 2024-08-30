from django.contrib import admin
from .models import Content
from apps.users.models import UserProfile
from django.utils.html import format_html

# Register your models here.

from import_export import resources
from import_export.admin import ImportExportModelAdmin, ImportExportActionModelAdmin


class ProxyResource(resources.ModelResource):
    class Meta:
        model = Content


class ContentModelsAdmin(ImportExportActionModelAdmin):
    resource_class = ProxyResource
    list_display = ['id', 'c_content_abstract', 'c_author_info', 'nLike', 'nComment',  'createTime']
    ordering = ('-priority',)
    fields_options = {
        'c_content_abstract': {
            'width': '500px',
        },
        'c_author_info': {
            'width': '250px'
        },
        'nLike': {
            'width': '110px'
        },
        'nComment': {
            'width': '110px'
        },
        'createTime': {
            'width': '170px'
        },
        'state': {
            'width': '110px'
        },
        'priority': {
            'width': '110px'
        }
    }
    list_filter = ['state', 'createTime']
    search_fields = ['id', 'contentText', 'openId']
    list_per_page = 100

    def c_content_abstract(self, obj):

        return format_html(
            '<span style="display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 3;overflow:'
            ' hidden;"">{}</span>',
            obj.contentText,
        )
    c_content_abstract.short_description = '内容'

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


admin.site.register(Content, ContentModelsAdmin)
