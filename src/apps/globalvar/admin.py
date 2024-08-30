from django.contrib import admin
from .models import GlobalVar
from django.utils.html import format_html

# Register your models here.


class GlobalVarAdmin(admin.ModelAdmin):
    list_display = ['key', 'c_value', 'help_text']
    search_fields = ['key', 'value', 'help_text']

    fields_options = {
        'key': {
            'width': '200px',
        },
        'value': {
            'width': '300px'
        },
        'help_text': {
            'width': '500px'
        },
    }

    def c_value(self, obj):

        return format_html(
            '<span style="display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 1;overflow:'
            ' hidden;"">{}</span>',
            obj.value,
        )
    c_value.short_description = '值'


admin.site.register(GlobalVar, GlobalVarAdmin)

