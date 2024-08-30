from django.contrib import admin

# Register your models here.

from .models import ColdUser, ColdContent, KeyWords


class ColdUserAdmin(admin.ModelAdmin):
    list_display = ['xh', 'delta']


admin.site.register(ColdUser, ColdUserAdmin)


class ColdContentAdmin(admin.ModelAdmin):
    list_display = ['contentId', 'page_number']


admin.site.register(ColdContent, ColdContentAdmin)


class KeyWordsAdmin(admin.ModelAdmin):
    list_display = ['keyword', 'valid_time_to', 'remark']


admin.site.register(KeyWords, KeyWordsAdmin)

