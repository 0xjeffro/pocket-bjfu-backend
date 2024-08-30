from django.contrib import admin
from .models import ChangYongLianJie

# Register your models here.


class ChangYongLianJieAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'desc', 'url', 'priority']
    search_fields = ['title', 'desc']


admin.site.register(ChangYongLianJie, ChangYongLianJieAdmin)
