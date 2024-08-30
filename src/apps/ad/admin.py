from django.contrib import admin
from .models import DefaultAD, ADLog
from django.utils.html import format_html

# Register your models here.


class DefaultADAdmin(admin.ModelAdmin):
    list_display = ['id', 'c_ad_img', 'c_ad_text', 'c_tag_a_text', 'c_tag_b_text', 'c_button', 'valid_time']
    list_filter = ['feature_sex', 'type', ]
    search_fields = ['ad_text', 'tag_a_text', 'tag_b_text', 'button_text', 'additional_field_a', 'additional_field_b']
    fields_options = {
        'id': {
            'width': '100px',
        },
        'c_ad_img': {
            'width': '100px'
        },
        'c_ad_text': {
            'width': '210px'
        },
        'c_tag_a_text': {
            'width': '100px'
        },
        'c_tag_b_text': {
            'width': '100px'
        },
        'c_button': {
            'width': '180px'
        },
        'valid_time': {
            'width': '170px'
        },
    }

    def c_ad_img(self, obj):

        return format_html(
            '<img src="{}" height="40" />',
            obj.ad_img,
        )
    c_ad_img.short_description = '广告图'

    def c_ad_text(self, obj):
        return format_html(
            '<span style="display: -webkit-box; -webkit-box-orient: vertical; -webkit-line-clamp: 2;overflow:'
            ' hidden;"">{}</span>',
            obj.ad_text,
        )

    c_ad_text.short_description = '广告文字'

    def c_tag_a_text(self, obj):
        return format_html(
            '<span style="color: {0}">{1}</span>',
            obj.tag_a_color,
            obj.tag_a_text,
        )
    c_tag_a_text.short_description = '标签A'

    def c_tag_b_text(self, obj):
        return format_html(
            '<span style="color: {0}">{1}</span>',
            obj.tag_b_color,
            obj.tag_b_text,
        )
    c_tag_b_text.short_description = '标签B'

    def c_button(self, obj):
        return format_html(
            '<div style="background-color: {0}; border-radius: 10px; color: #fff; '
            'margin-left: 10px; margin-right: 0px; width: auto;"> {1} </div>',
            obj.button_color,
            obj.button_text,
        )
    c_button.short_description = '引导按钮'


admin.site.register(DefaultAD, DefaultADAdmin)


class ADLogAdmin(admin.ModelAdmin):
    list_display = ['id', 'ad_id', 'openId', 'createTime']
    search_fields = ['ad_id', 'openId']
    list_filter = ['createTime', ]


admin.site.register(ADLog, ADLogAdmin)
