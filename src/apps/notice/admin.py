from django.contrib import admin
from .models import Notice
from django.utils.html import format_html

# Register your models here.


class NoticeAdmin(admin.ModelAdmin):
    ordering = ('-priority', )
    list_display = ['priority', 'content', 'xh_startswith', 'mode', 'to_type', 'show']
    list_filter = ['component', ]
    fields_options = {
        'priority': {
            'width': '100px',
        },
        'content': {
            'width': '810px'
        },
        'xh_startswith': {
            'width': '100px'
        },
        'mode': {
            'width': '100px'
        },
        'to_type': {
            'width': '100px'
        },
        'show': {
            'width': '100px'
        }
    }


admin.site.register(Notice, NoticeAdmin)
