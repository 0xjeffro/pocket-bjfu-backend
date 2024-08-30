from django.contrib import admin
from .models import JiaoWuChuNews

# Register your models here.


class JiaoWuChuNewsAdmin(admin.ModelAdmin):
    list_display = ['title', 'time', 'url', ]
    search_fields = ['title', 'url', 'pic_url']
    list_filter = ['time', ]
    list_per_page = 5


admin.site.register(JiaoWuChuNews, JiaoWuChuNewsAdmin)

